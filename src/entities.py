from uuid import UUID, uuid4
from math import pi, sin

import Common
import vision
import Memory

from Config import ConfigData

class Entity:
    
    # What the entity is:
    specie : Common.Species.BaseSpecie
    genome : Common.Genomes.Genome
    
    # How the entity acts:
    eyes : vision.Vision
    memory : Memory.Memory

    # State
    __is_alive : bool
    __day_born : int
    reproductive_urge : float
    hunger : float

    # If entity has no targets
    fallback_location : tuple[float, float] | None
    
    # Static stuff
    max_hunger : float

    # Metadata
    __uuid : UUID
    
    def __init__(self, specie: Common.Species.BaseSpecie, genome : Common.Genomes.Genome, hunger : float, cur_day : int, config: ConfigData.Config) -> None:
        self.specie = specie
        self.genome = genome

        self.eyes = vision.Vision(self.genome.vision_range.value * config.Simulation.grid_size)
        self.memory = Memory.Memory(config.Entities.short_term_memory_span, config.Entities.long_term_memory_span, cur_day)

        self.__is_alive = True
        self.__day_born = cur_day # TODO Convert to timestamp of global time, when born.
        self.reproductive_urge = 0.2
        self.hunger = hunger

        self.fallback_location = None
        
        self.max_hunger = -sin(pi * self.genome.speed.value - (pi/2)) + 1 # https://www.desmos.com/calculator/ph8iwacdps

        self.__uuid = uuid4()
    
    def identify_multiple_relationships(self, other_entities : list["Entity"]) -> dict[Common.Species.SpecieRelationship, list["Entity"]]:
        identified = {
            Common.Species.SpecieRelationship.PREDATOR : [],
            Common.Species.SpecieRelationship.NEUTRAL : [],
            Common.Species.SpecieRelationship.PREY : [],
            Common.Species.SpecieRelationship.CONGENER : [],
        }
        for other in other_entities:
            identified[self.specie.identify_relationship(other.specie)].append(other)
        return identified


    def export_dict(self) -> dict:
        return {
            "uuid": self.uuid,
            "species": self.specie.export_dict(),
            "genome": self.genome.export_dict(),
            "memory": self.memory.export_dict(),
            "is_alive": self.is_alive,
            "hunger": self.hunger,
        }

    def age(self, current_day : int) -> int:
        return current_day - self.__day_born
    
    def kill(self) -> None:
        self.__is_alive = False
    
    @property
    def uuid(self) -> str:
        return str(self.__uuid)
    
    @property
    def can_move(self) -> bool:
        return self.specie.can_move
    
    @property
    def can_see(self) -> bool:
        return self.specie.can_see
    
    @property
    def day_born(self) -> int:
        return self.__day_born

    @property
    def is_alive(self) -> bool:
        return self.__is_alive

    def __repr__(self) -> str:
        return f"Entity; uuid:{str(self.__uuid)}"
    
    def __hash__(self) -> int:
        return hash(str(self.__uuid))