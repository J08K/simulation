from entities import Entity
import Common

class Board:

    __width : int
    __height : int
    
    entities : dict[Entity, tuple[float, float]]

    def __init__(self, board_width : int, board_height : int) -> None:
        self.__width = board_width
        self.__height = board_height
        self.entities = dict()

        # * For now just storing all entities and their locations.
        # * This requires looping over every entity for every entity, so O(n^2) every time.
        # TODO Might want to make it so that it's split up in districts.
        # * This would make it so that there is only a need to check for in an enities current district and neightbouring districts.

    def set_entity(self, entity : Entity, location : tuple[float, float]) -> None:
        if not self.in_bounds(location):
            x_pos, y_pos = location
            raise ValueError(f"Location ({x_pos}, {y_pos}) is out of bounds!")
        self.entities[entity] = location

    def in_bounds(self, location : tuple[float, float]) -> bool:
        x_pos, y_pos = location
        return 0 <= x_pos <= self.max_x_coord and 0 <= y_pos <= self.max_y_coord

    def get_all_in_view(self, current_entity : Entity) -> list[Entity]:
        """Returns a generator that gets all entities in view of current_entity's vision."""
        current_coords = self.entities[current_entity]
        for target_entity, target_coords in self.entities.items():
            if target_entity != current_entity:
                if current_entity.eyes.abs_in_view(cur_coords=current_coords, target_coords=target_coords):
                    yield target_entity

    def get_entity_location(self, entity : Entity) -> tuple[float, float]:
        if entity in self.entities:
            return self.entities[entity]
        else:
            raise ValueError(f"Entity was not found! [{str(entity)}]") # TODO Output this to logger.

    @property
    def max_x_coord(self) -> int:
        return self.__width - 1
    
    @property
    def max_y_coord(self) -> int:
        return self.__height - 1

    def __len__(self) -> int:
        return len(self.entities)

    def __repr__(self) -> str:
        output : list[str] = []
        output.append("+" + "-" * (self.__width * 2) + "+\n")
        
        lines = [["  " for _ in range(self.__width)] for _ in range(self.__height)]

        for entity in self.entities.keys():
            pos_x, pos_y = self.entities[entity]
            pos_x = round(pos_x)
            pos_y = round(pos_y)
            lines[pos_y][pos_x] = Common.fixed_size_string(str(entity.specie.id), 2)

        for line in lines:
            output.append("|" + "".join(line) + "|\n")

        output.append("+" + "-" * (self.__width * 2) + "+")
        return "".join(output)

if __name__ == "__main__":
    import random

    test_board = Board(20, 20)
    for _ in range(20):
        test_pos = random.randint(0, test_board.max_x_coord), random.randint(0, test_board.max_x_coord)
        test_board.set_entity(Entity(
            specie=Common.Species.BaseSpecie(random.randint(0, 3), "test", [1, 2, 3], True, True),
            genome=Common.Genomes.Genome(
                speed_gene=Common.Genomes.Gene("speed", 0.5, 0.2),
                hunger_rate_gene=Common.Genomes.Gene("hunger_rate", 0.5, 0.2),
                max_hunger_gene=Common.Genomes.Gene("max_hunger", 0.5, 0.2),
                vision_range_gene=Common.Genomes.Gene("vision_range", 0.5, 0.2),
                gestation_period_gene=Common.Genomes.Gene("gestation_period", 0.5, 0.2),
            ),
            cur_day=0
        ), test_pos)
    print(test_board.entities)
    print(len(test_board))
    print(test_board)