import new_board

from uuid import uuid4

if __name__ == "__main__":
    brd = new_board.Board(16.0, 10.0, 3.0)
    
    for row_idx in range(len(brd.sub_grids[0])):
        print(" ".join(repr(col[::-1][row_idx]) for col in brd.sub_grids))
    
    print()
    
    locations = [
        (1.5, 1.5),
        (3.5, 2.3),
        (8.3, 0.8),
        (13.1, 0.8),
        (5.3, 4.3),
        (9.1, 4.3),
        (13.1, 4.1),
        (2.1, 6.6),
        (6.8, 8.3),
        (10.3, 7.2),
        (15.1, 9.1),
    ]
    for x, y in locations:
        brd.add_entity(uuid4(), x, y)
    
    for row_idx in range(len(brd.sub_grids[0])):
        print(" ".join(repr(col[::-1][row_idx]) for col in brd.sub_grids))