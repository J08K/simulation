import math
import Common


def get_max_values(entity_x : int, entity_y : int, view_range : float, board_max_x : int, board_max_y : int) -> tuple[int, int, int, int]:
    # Optimizations, so that it doesn't have to check for every coord on the board.
    # TODO Cache this maybe?
    view_max_x = Common.clamp(0, board_max_x, entity_x + view_range)
    view_min_x = Common.clamp(0, board_max_x, entity_x - view_range)

    view_max_y = Common.clamp(0, board_max_y, entity_y + view_range)
    view_min_y = Common.clamp(0, board_max_y, entity_y - view_range)
    
    return view_min_x, view_max_x, view_min_y, view_max_y

def in_view_circle(x : int, y : int, r : float, a : float) -> bool:
    # 'a' in radians.
    
    # Formula based on https://www.desmos.com/calculator/kux33fukmq
    cutoff = a * x

    y = -y if y < 0 else y # * So we don't get any negative y_numbers.
    
    main_formula = math.sqrt(-x ** 2 + r ** 2) - y >= 0
    secondary = y <= cutoff if a > 0 else y >= cutoff

    # TODO in_view_circle(-1, 1, 3, degrees_to_slope(135)) should == True

    return main_formula and secondary
    

def get_seeable_coord(entity_x : int, entity_y : int, view_range : float, view_fov_degrees : float, board_max_x : int, board_max_y : int, entity_rotation : int) -> list[tuple[int, int]]:

    # TODO Implement this into a class, just like the RegionVision class.

    view_min_x, view_max_x, view_min_y, view_max_y = get_max_values(entity_x, entity_y, view_range, board_max_x, board_max_y)

    coords = []
    
    cutoff_slope = Common.Rotation.degrees_to_slope(view_fov_degrees)
    
    # TODO Add ability to rotate.
    
    for x in range(view_min_x, view_max_x + 1):
        
        for y in range(view_min_y, view_max_y + 1):
            
            is_in_view = in_view_circle(x, y, view_range, cutoff_slope)

            # TODO Finish this... I don't really remember exactly what I was doing :P

class Vision:
    
    def abs_in_view(self, cur_coords : tuple[float, float], target_coords : tuple[float, float]) -> bool:
        ...

class RangeVision(Vision):
    
    __distance : float
    
    def __init__(self, view_distance : float) -> None:
        super().__init__()
        self.__distance = view_distance
        
    def abs_in_view(self, cur_coords : tuple[float, float], target_coords : tuple[float, float]) -> bool:
        cur_x, cur_y = cur_coords
        target_x, target_y = target_coords
        return Common.calc_distance(cur_x, cur_y, target_x, target_y) <= self.__distance
    
    def rel_in_view(self, target_coords : tuple[float, float]) -> bool:
        target_x, target_y = target_coords
        return Common.calc_distance(0.0, 0.0, target_x, target_y)