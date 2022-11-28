from entities import Entity
import common

class Board:

    __width : int
    __height : int
    
    entities : dict[Entity, tuple[float, float]]

    def __init__(self, board_width : int, board_height : int) -> None:
        self.__width = board_width
        self.__height = board_height
        self.entities = dict()

        # * For now just storing all entities and their locations.
        # * This requires looping over every entity...
        # ! Not very efficient.

    def add_entity(self, entity : Entity, location : tuple[float, float]) -> None:
        x_pos, y_pos = location
        if x_pos > self.max_x_coord or y_pos > self.max_y_coord:
            raise ValueError(f"Location ({x_pos}, {y_pos}) is out of bounds!")
        self.entities[entity] = location

    @property
    def max_x_coord(self) -> int:
        return self.__width - 1
    
    @property
    def max_y_coord(self) -> int:
        return self.__height - 1

    def __len__(self) -> int:
        return len(self.entities)

    def __repr__(self) -> str:
        output = []
        output.append("+" + "-" * (self.__width * 2) + "+\n")
        
        lines = [["  " for _ in range(self.__width)] for _ in range(self.__height)]

        for entity in self.entities.keys():
            pos_x, pos_y = self.entities[entity]
            pos_x = round(pos_x)
            pos_y = round(pos_y)
            lines[pos_y][pos_x] = common.fixed_size_string(str(entity.species), 2)

        for line in lines:
            output.append("|" + "".join(line) + "|\n")

        output.append("+" + "-" * (self.__width * 2) + "+")
        return "".join(output)

import random

test_board = Board(10, 10)
test_entities = []
for _ in range(20):
    test_pos = random.randint(0, test_board.max_x_coord), random.randint(0, test_board.max_x_coord)
    test_board.add_entity(Entity(
        species=random.randint(0, 2),
        entity_type=random.randint(0, 1),
        max_health=random.randint(0, 100),
        can_move=True,
        can_see=True,
        cur_day=0
    ), test_pos)
print(test_board.entities)
print(len(test_board))
print(test_board)