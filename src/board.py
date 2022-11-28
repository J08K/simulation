from entities import Entity
class Board:

    __width : int
    __height : int
    
    entities : dict[Entity, tuple[float, float]]

    def __init__(self, board_width : int, board_height : int) -> None:
        self.__width = board_width
        self.__height = board_height

        # * For now just storing all entities and their locations.
        # * This requires looping over every entity...
        # ! Not very efficient.