from enum import Enum
from uuid import UUID, uuid4

from common import Rotation

class EntityType(Enum):
    plant = 0
    animal = 1

class EntitySpecies(Enum):
    plant = 0
    prey = 1
    predator = 2

class Entity:
    
    species : EntitySpecies
    
    max_health : str
    health : int

    __entity_type : EntityType
    __day_born : int
    __uuid : UUID
    
    # Abilities
    __can_move : bool
    __can_see : bool
    
    def __init__(self, species: EntitySpecies, entity_type: EntityType, max_health : int, can_move : bool, can_see : bool, cur_day : int) -> None:
        self.species = species
        self.max_health = max_health
        self.health = max_health

        self.__can_move = can_move
        self.__can_see = can_see

        self.__entity_type = entity_type
        self.__uuid = uuid4
        self.__day_born = cur_day
    
    def lifetime(self, current_day : int) -> int:
        return current_day - self.__day_born
    
    @property
    def uuid(self) -> str:
        return str(self.__uuid)
    
    @property
    def can_move(self) -> bool:
        return self.__can_move
    
    @property
    def can_see(self) -> bool:
        return self.__can_see
    
    @property
    def day_born(self) -> int:
        return self.__day_born

    @property
    def entity_type(self) -> EntityType:
        return self.__entity_type

class PlantEntity(Entity):
    
    def __init__(self, species: EntitySpecies, max_health : int, cur_day : int) -> None:
        super().__init__(
            species=species,
            entity_type=EntityType.plant,
            max_health=max_health,
            can_move=False,
            can_see=False,
            cur_day=cur_day
            )
        

class AnimalEntity(Entity):
    
    __can_eat : list[EntitySpecies]

    rotation : Rotation
    view_range : float
    view_fov : float
    
    def __init__(self, species: EntitySpecies, max_health: int, cur_day : int, view_range : float, view_fov : float) -> None:
        super().__init__(species, EntityType.animal, max_health, True, True, cur_day)
        self.view_fov = view_fov
        self.view_range
        self.rotation = Rotation.NORTH
        
    def can_eat_entity(self, target_entity : Entity) -> bool:
        """Returns whether this Entity can eat target_entity.

        Args:
            target_entity (Entity): Target entity

        Returns:
            bool: Whether the 'entity' can be eaten by this entity.
        """
        return target_entity.species in self.__can_eat
    
    def return_view(self, view : list[tuple[int, int, Entity]]) -> None:
        ...