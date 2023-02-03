"""New board design, to make looping over entities more efficient."""

import math

from uuid import UUID



class OutOfBoundsError(Exception):
    """Raised when a given location is out of bounds for a grid."""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class SubGrid:
    
    __width : float
    __height : float
    
    grid_entities : dict[UUID, tuple[float, float]]
    
    def __init__(self, width : float, height : float) -> None:
        self.__width = width
        self.__height = height
        self.grid_entities = dict()
    
    def change_entity_data(self, entity : UUID, x : float, y : float) -> None:
        self.grid_entities[entity] = (x, y)
    
    def get_entity_location(self, entity : UUID) -> tuple[float, float] | None:
        if entity in self.grid_entities:
            return self.grid_entities[entity]
        return None
    
    def get_all_entities(self) -> list[tuple[UUID, float, float]]:
        return [(entity, *location) for entity, location in self.grid_entities.items()]

    def __repr__(self) -> str:
        return f"<SubGrid width={self.__width} height={self.__height} entities={len(self.grid_entities)}>"

    @property
    def count(self) -> int:
        return len(self.grid_entities)

class Board:

    # A board contains many sub-grids, this should help more efficiently looping over entities.
    
    __width : float # TODO Add property
    __height : float # TODO Add property
    __max_view_distance : float # TODO Add property
    
    sub_grids : list[list[SubGrid]] # Stores grids, by their (x, y) location.
    
    entity_registry : dict[UUID, tuple[int, int]] # Stores each entity's current grid. Quick and dirty lookup basically.
    
    def __init__(self, width : float, height : float, max_view_distance : float) -> None:
        self.__width = width
        self.__height = height
        self.__max_view_distance = max_view_distance
        self.entity_registry = {}
        self.sub_grids = []
        
        self.new_sub_grids(transfer_data=False)
    
    def new_sub_grids(self, transfer_data : bool) -> None:
        # TODO if need for recalculating grids, transfer the data from the old grids to the new grids.
        
        num_width_full_grids = int(self.__width // self.__max_view_distance) # Amount of full-sized grids in the x direction.
        num_height_full_grids = int(self.__height // self.__max_view_distance) # Amount of full-sized grids in the y direction.

        width_column_partial_grids = self.__width % self.__max_view_distance # Width of column of leftover grid size.
        height_row_partial_grids = self.__height % self.__max_view_distance # Height of row of leftover grid size.
        
        sub_grids : list[list[SubGrid]] = []
        for column_idx in range(num_width_full_grids): # Starting in the x direction
            column_sub_grids : list[SubGrid] = []
            for row_idx in range(num_height_full_grids):
                column_sub_grids.append(SubGrid(
                    width=self.__max_view_distance,
                    height=self.__max_view_distance,
                ))
            
            if height_row_partial_grids:
                column_sub_grids.append(SubGrid(
                    width=self.__max_view_distance,
                    height=height_row_partial_grids
                ))
            
            sub_grids.append(column_sub_grids)
        
        if width_column_partial_grids:
            sub_grids.append([
                    SubGrid(
                        width=width_column_partial_grids, # Honestly kind of hate this formatting :P
                        height=self.__max_view_distance,
                    ) for _ in range(num_height_full_grids)
                ])
        
        if width_column_partial_grids and height_row_partial_grids:
            sub_grids[-1].append(SubGrid(
                width=width_column_partial_grids,
                height=height_row_partial_grids,
            ))
        self.sub_grids = sub_grids


    def get_neighbour_grids(self, grid_x : int, grid_y : int) -> list[tuple[int, int]]:
        neighbours = []
        for idx in range(8):
            neighbour_x = grid_x + round(math.cos(0.25 * idx * math.pi))
            neighbour_y = grid_y + round(math.sin(0.25 * idx * math.pi))
            # TODO What happens if there is not grid at index 0?
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
        if entity_x > self.__width or entity_y > self.__height:
            raise OutOfBoundsError(f"Location ({entity_x}, {entity_y}) is out of bounds! Maximum is ({self.__width}, {self.__height})!")
        
        return int(entity_x // self.__max_view_distance), int(entity_y // self.__max_view_distance)


    def add_entity(self, entity : UUID, x : float, y : float) -> None:
        if x > self.__width or y > self.__height:
            raise OutOfBoundsError(f"Location ({x}, {y}) is out of bounds! Maximum is ({self.__width}, {self.__height})!")
        
        grid_location = self.grid_from_entity_loc(x, y)
        target_grid = self.get_grid(*grid_location)
        self.entity_registry[entity] = grid_location
        target_grid.change_entity_data(entity, x, y)


    def get_entities_nearby(self, entity : UUID) -> None:
        if entity not in self.entity_registry:
            raise ValueError("Entity not found on board!")
        current_grid_coords = self.entity_registry[entity]
        found_entities = [(new_entity, x, y)for new_entity, x, y in self.get_grid(*current_grid_coords).get_all_entities() if new_entity != entity]
        for neighbour in self.get_neighbour_grids(*current_grid_coords):
            found_entities += self.get_grid(*neighbour).get_all_entities()
        return found_entities


    def get_entity_location(self, entity : UUID) -> tuple[float, float]:
        if entity not in self.entity_registry:
            raise ValueError("Entity not found on board!")
        grid_x, grid_y = self.entity_registry[entity]
        return self.sub_grids[grid_x][grid_y].get_entity_location(entity)


    @property
    def all_entities(self) -> list[UUID]:
        return [entity for entity in self.entity_registry.keys()]


    @property
    def num_entities(self) -> int:
        return sum([sub_grid.count for sub_grid, _ in self.iter_grids()])