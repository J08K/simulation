import math

def clamp(min_n : int, max_n : int, n : int) -> int:
    n = max(n, min_n)
    n = min(n, max_n)
    return n

def get_max_values(entity_x : int, entity_y : int, view_range : float, board_max_x : int, board_max_y : int) -> tuple[int, int, int, int]:
    # Optimizations, so that it doesn't have to check for every coord on the board.
    # TODO Cache this maybe?
    view_max_x = clamp(0, board_max_x, entity_x + view_range)
    view_min_x = clamp(0, board_max_x, entity_x - view_range)

    view_max_y = clamp(0, board_max_y, entity_y - view_range)
    view_min_y = clamp(0, board_max_y, entity_y + view_range)
    
    return view_min_x, view_max_x, view_min_y, view_max_y

def in_view_circle(x : int, y : int, r : float, a : float) -> bool:
    # 'a' in radians.
    
    

def get_seeable_coord(entity_x : int, entity_y : int, view_range : float, view_fov_degrees : float, board_max_x : int, board_max_y : int, entity_rotation : int) -> list[tuple[int, int]]:

    view_min_x, view_max_x, view_min_y, view_max_y = get_max_values(entity_x, entity_y, view_range, board_max_x, board_max_y)
    
    coords = []
    
    view_fov_radians = math.tan(view_fov_degrees * (math.pi / 180))
    
    # TODO Add ability to rotate.
    
    for x in range(view_min_x, view_max_x + 1):
        
        for y in range(view_min_y, view_max_y + 1):
            
            is_in_view = math.sqrt(-x ** 2 + view_range ** 2)