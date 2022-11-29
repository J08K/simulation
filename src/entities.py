from enum import Enum
from uuid import UUID, uuid4

import Common

class EntityType(Enum):
    plant = 0
    animal = 1

class Entity:
    
    species : Common.Species.BaseSpecie
    
    is_alive : bool

    genome : Common.Genomes.Genome
    vision : vision.RegionVision

    __day_born : int
    __uuid : UUID
    
    # Abilities
    __can_move : bool
    __can_see : bool
    
    def __init__(self, species: Common.Species.BaseSpecie, max_health : int, can_move : bool, can_see : bool, cur_day : int) -> None:
        self.species = species
        self.max_health = max_health
        self.health = max_health

        self.__can_move = can_move
        self.__can_see = can_see
        self.__day_born = cur_day

        self.__uuid = uuid4()
    
    def age(self, current_day : int) -> int:
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

    def __repr__(self) -> str:
        return f"Entity; uuid:{str(self.__uuid)}"
    
    def __hash__(self) -> str:
        return hash(str(self.__uuid))