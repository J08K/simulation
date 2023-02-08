import Common

from typing import Generator, Any

class Vision:

    """Responsible for observing the environment around the parent Entity.

    """
    
    __distance : float
    
    def __init__(self, view_distance : float) -> None:
        self.__distance = view_distance
    
    def abs_in_view(self, cur_coords : tuple[float, float], target_coords : tuple[float, float]) -> bool:
        """Tests whether the absolute target coordinates are in view of the entity."""
        cur_x, cur_y = cur_coords
        target_x, target_y = target_coords
        return Common.calc_distance(cur_x, cur_y, target_x, target_y) <= self.__distance
        
    def rel_in_view(self, target_coords : tuple[float, float]) -> bool:
        """Tests whether the relative target coordinates are in view of the entity."""
        return self.abs_in_view((0.0, 0.0), target_coords)

    def iter_visible_entities(self, cur_coords : tuple[float, float], entities : dict) -> Generator[tuple[Any, tuple[float, float]], None, None]:
        for entity, entity_coords in entities.items():
            if self.abs_in_view(cur_coords, entity_coords):
                yield entity, entity_coords

    def dict_visible_entities(self, cur_coords : tuple[float, float], entities : dict) -> dict[Any, tuple[float, float]]:
        return {entity : value for entity, value in self.iter_visible_entities(cur_coords, entities)}

    @property
    def view_distance(self) -> float:
        return self.__distance