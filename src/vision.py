import Common
import entities

class Vision:
    
    __distance : float
    
    def __init__(self, view_distance : float) -> None:
        self.__distance = view_distance
    
    def abs_in_view(self, cur_coords : tuple[float, float], target_coords : tuple[float, float]) -> bool:
        cur_x, cur_y = cur_coords
        target_x, target_y = target_coords
        return bool(Common.calc_distance(cur_x, cur_y, target_x, target_y) <= self.__distance)
        
    def rel_in_view(self, target_coords : tuple[float, float]) -> bool:
        return self.abs_in_view((0.0, 0.0), target_coords)

    def visible_entities(self, entities : dict[entities.Entity, tuple[float, float]]) -> dict[entities.Entity, tuple[float, float]]:
        ...

    @property
    def view_distance(self) -> float:
        return self.__distance