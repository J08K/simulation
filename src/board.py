"""New board design, to make looping over entities more efficient."""

import Common
import math

from entities import Entity


class OutOfBoundsError(Exception):
    """Raised when a given location is out of bounds for a grid."""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GridError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class EntityNotFoundError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class SubGrid:
    
    __width : float
    __height : float
    
    grid_entities : dict[Entity, tuple[float, float]]
    
    def __init__(self, width : float, height : float) -> None:
        self.__width = width
        self.__height = height
        self.grid_entities = dict()
    
    def change_entity_data(self, entity : Entity, x : float, y : float) -> None:
        self.grid_entities[entity] = (x, y)
    
    def get_entity_location(self, entity : Entity) -> tuple[float, float] | None:
        if entity in self.grid_entities:
            return self.grid_entities[entity]
        return None
    
    def pop_entity(self, entity : Entity) -> tuple[float, float]:
        if entity not in self.grid_entities:
            raise EntityNotFoundError(f"Entity '{str(entity)}' is not in grid!")
        
        return self.grid_entities.pop(entity)

    def get_all_entities(self) -> list[tuple[Entity, float, float]]:
        return [(entity, *location) for entity, location in self.grid_entities.items()]

    def __repr__(self) -> str:
        return f"<SubGrid width={self.__width} height={self.__height} entities={len(self.grid_entities)}>"

    @property
    def count(self) -> int:
        return len(self.grid_entities)


class Board:

    # A board contains many sub-grids, this should help more efficiently looping over entities.
    
    __width : float
    __height : float
    __grid_size : float
    
    sub_grids : list[list[SubGrid]] # Stores grids, by their (x, y) location.
    
    entity_registry : dict[Entity, tuple[int, int]] # Stores each entity's current grid. Quick and dirty lookup basically.
    
    def __init__(self, width : float, height : float, grid_size : float) -> None:
        self.__width = width
        self.__height = height
        self.__grid_size = grid_size
        self.entity_registry = {}
        self.sub_grids = []
        
        self.new_sub_grids(transfer_data=False)
    
    def new_sub_grids(self, transfer_data : bool) -> None:
        cached_entities = {}
        if transfer_data:
            cached_entities = {entity: self.get_entity_location(entity) for entity in self.all_entities}

        self.entity_registry = {}

        num_width_full_grids = int(self.__width // self.__grid_size) # Amount of full-sized grids in the x direction.
        num_height_full_grids = int(self.__height // self.__grid_size) # Amount of full-sized grids in the y direction.

        width_column_partial_grids = self.__width % self.__grid_size # Width of column of leftover grid size.
        height_row_partial_grids = self.__height % self.__grid_size # Height of row of leftover grid size.

        sub_grids : list[list[SubGrid]] = []
        for _ in range(num_width_full_grids): # Starting in the x direction
            column_sub_grids : list[SubGrid] = []
            for _ in range(num_height_full_grids):
                column_sub_grids.append(SubGrid(
                    width=self.__grid_size,
                    height=self.__grid_size,
                ))
            
            if height_row_partial_grids:
                column_sub_grids.append(SubGrid(
                    width=self.__grid_size,
                    height=height_row_partial_grids
                ))
            
            sub_grids.append(column_sub_grids)
        
        if width_column_partial_grids:
            sub_grids.append([
                    SubGrid(
                        width=width_column_partial_grids, # Honestly kind of hate this formatting :P
                        height=self.__grid_size,
                    ) for _ in range(num_height_full_grids)
                ])
        
        if width_column_partial_grids and height_row_partial_grids:
            sub_grids[-1].append(SubGrid(
                width=width_column_partial_grids,
                height=height_row_partial_grids,
            ))
        self.sub_grids = sub_grids

        if transfer_data:
            for entity, (x, y) in cached_entities.items():
                self.add_entity(
                    entity=entity,
                    x=x,
                    y=y
                )


    def in_bounds(self, x : float, y : float) -> bool:
        return 0 <= x <= self.width and 0 <= y <= self.height


    def get_neighbour_grids(self, grid_x : int, grid_y : int) -> list[tuple[int, int]]:
        neighbours = []
        for idx in range(8):
            neighbour_x = grid_x + round(math.cos(0.25 * idx * math.pi))
            neighbour_y = grid_y + round(math.sin(0.25 * idx * math.pi))

            if len(self.sub_grids) == 0:
                raise GridError("There are no grids on this board.")
            if len(self.sub_grids[0]) == 0:
                raise GridError("This board is invalid! Did you touch 'sub_grids'?")

            if neighbour_x >= 0 and neighbour_y >= 0 and neighbour_x < len(self.sub_grids) and neighbour_y < len(self.sub_grids[0]):
                neighbours.append((neighbour_x, neighbour_y))
        return neighbours


    def get_grid(self, grid_x : int, grid_y : int) -> SubGrid:
        return self.sub_grids[grid_x][grid_y]


    def iter_grids(self) -> tuple[SubGrid, tuple[int, int]]:
        for x, column in enumerate(self.sub_grids):
            for y, grid in enumerate(column):
                yield grid, (x, y)


    def grid_from_entity_loc(self, entity_x : float, entity_y : float) -> tuple[int, int]:
        """Calculate what grid an entity should be in by its x and y coordinates."""
        # TODO Change naming of this, might not just be used for entity locations, but also just for finding out what location a grid contains.
        if entity_x > self.__width or entity_y > self.__height:
            raise OutOfBoundsError(f"Location ({entity_x}, {entity_y}) is out of bounds! Maximum is ({self.__width}, {self.__height})!")
        
        return int(entity_x // self.__grid_size), int(entity_y // self.__grid_size)


    def add_entity(self, entity : Entity, x : float, y : float) -> None:
        """For an entity to be added to the grid. If you want to edit entity location, use 'set_entity_location()'"""
        if not self.in_bounds(x, y):
            raise OutOfBoundsError(f"Location ({x}, {y}) is out of bounds! Maximum is ({self.__width}, {self.__height})!")
        
        grid_location = self.grid_from_entity_loc(x, y)
        target_grid = self.get_grid(*grid_location)
        self.entity_registry[entity] = grid_location
        target_grid.change_entity_data(entity, x, y)


    def set_entity_location(self, entity : Entity, x : float, y : float) -> None:
        """Change the location of an entity."""
        if not self.in_bounds(x, y):
            raise OutOfBoundsError(f"Location ({x}, {y}) is out of bounds! Maximum is ({self.__width}, {self.__height})!")
        
        if entity not in self.entity_registry:
            raise EntityNotFoundError(f"Entity '{str(entity)}' is not present in the registry.")

        entity_current_grid = self.entity_registry[entity]
        entity_new_grid = self.grid_from_entity_loc(x, y)
        new_grid = self.get_grid(*entity_new_grid)
        if entity_current_grid != entity_new_grid:
            # If grid has changed, remove the entity from the old grid, and change their grid in the registry.
            self.get_grid(*entity_current_grid).pop_entity(entity)
            self.entity_registry[entity] = new_grid
        new_grid.change_entity_data(entity, x, y)


    def get_entities_nearby(self, entity : Entity) -> list[tuple[Entity. float, float]]:
        if entity not in self.entity_registry:
            raise EntityNotFoundError(f"Entity '{str(entity)}' is not present in the registry.")
        
        current_grid_coords = self.entity_registry[entity]
        found_entities = [(new_entity, x, y)for new_entity, x, y in self.get_grid(*current_grid_coords).get_all_entities() if new_entity != entity]
        for neighbour in self.get_neighbour_grids(*current_grid_coords):
            found_entities += self.get_grid(*neighbour).get_all_entities()
        return found_entities


    def get_entity_location(self, entity : Entity) -> tuple[float, float]:
        if entity not in self.entity_registry:
            raise EntityNotFoundError(f"Entity '{str(entity)}' is not present in the registry.")
        grid_x, grid_y = self.entity_registry[entity]
        return self.sub_grids[grid_x][grid_y].get_entity_location(entity)


    def get_all_in_view(self, entity : Entity) -> dict[Entity, tuple[float, float]]:
        targets = self.get_entities_nearby(entity)
        cur_x, cur_y = self.get_entity_location(entity)
        
        visible = {}
        
        for other, target_x, target_y in targets:
            if Common.calc_distance(target_x, target_y, cur_x, cur_y) <= entity.eyes.view_distance:
                visible[other] = (target_x, target_y)

        return visible

    @property
    def all_entities(self) -> list[Entity]:
        return [entity for entity in self.entity_registry.keys()]


    @property
    def num_entities(self) -> int:
        return sum([sub_grid.count for sub_grid, _ in self.iter_grids()])


    @property
    def width(self) -> float:
        return self.__width


    @property
    def height(self) -> float:
        return self.__height


    @property
    def max_view_distance(self) -> float:
        return self.__grid_size


    @property
    def max_x_coord(self) -> float:
        return self.width


    @property
    def max_y_coord(self) -> float:
        return self.height


    @property
    def __len__(self) -> int:
        return self.num_entities

    # TODO get_all_in_view()