class Board:

    __width : int
    __height : int
    __num_sectors : int

    def __init__(self, board_width : int, board_height : int, amount_of_sectors : int) -> None:
        self.__width = board_width
        self.__height = board_height
        self.__num_sectors = amount_of_sectors

        # TODO Figure out a way to store entity locations.