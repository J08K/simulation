from typing import Any
from uuid import UUID, uuid4
from math import pi, sin

import Common
import vision
import Memory

from Config import ConfigData

class Entity:
    
    # TODO Track children.
    
    # What the entity is:
    specie : Common.Species.BaseSpecie
    genome : Common.Genomes.Genome
    
    # How the entity acts:
    eyes : vision.Vision
    memory : Memory.Memory

    # State
    __is_alive : bool
    __day_born : float
    reproductive_urge : float
    hunger : float
    
    # Pregnancy stuff
    pregnant_remaining: float | None
    other_parent_genome: Common.Genomes.Genome | None

    # If entity has no targets
    fallback_location : tuple[float, float] | None
    
    # Static stuff
    max_hunger : float

    config : ConfigData.Config

    # Metadata
    __uuid : UUID
    
    def __init__(self, specie: Common.Species.BaseSpecie, genome : Common.Genomes.Genome, hunger : float, cur_day : float, config: ConfigData.Config) -> None:
        self.specie = specie
        self.genome = genome

        self.eyes = vision.Vision(self.genome.vision_range.value * config.Simulation.grid_size)
        self.memory = Memory.Memory(config.Entities.short_term_memory_span, config.Entities.long_term_memory_span, cur_day)

        self.__is_alive = True
        self.__day_born = cur_day # TODO Convert to timestamp of global time, when born.
        self.reproductive_urge = 0.2
        self.hunger = hunger
        
        self.pregnant_remaining = None
        self.other_parent_genome = None

        self.fallback_location = None
        
        self.max_hunger = -sin(pi * self.genome.speed.value - (pi/2)) + 1 # https://www.desmos.com/calculator/ph8iwacdps
        self.config = config

        self.__uuid = uuid4()
    
    def identify_multiple_relationships(self, other_entities : list["Entity"]) -> dict[Common.Species.SpecieRelationship, list["Entity"]]:
        identified : dict[Common.Species.SpecieRelationship, list[Entity]] = {
            Common.Species.SpecieRelationship.PREDATOR : [],
            Common.Species.SpecieRelationship.NEUTRAL : [],
            Common.Species.SpecieRelationship.PREY : [],
            Common.Species.SpecieRelationship.CONGENER : [],
        }
        for other in other_entities:
            identified[self.specie.identify_relationship(other.specie)].append(other)
        return identified


    def export_dict(self) -> dict[str, Any]:
        return {
            "uuid": self.uuid,
            "species": self.specie.export_dict(),
            "genome": self.genome.export_dict(),
            "memory": self.memory.export_dict(),
            "is_alive": self.is_alive,
            "hunger": self.hunger,
        }
    
    def impregnate(self, other_parent_genome : Common.Genomes.Genome) -> None:
        self.other_parent_genome = other_parent_genome
        self.pregnant_remaining = self.genome.gestation_period.value * 10
        
    def birth_children(self, cur_time : float) -> list["Entity"]:
        if self.other_parent_genome != None and self.pregnant_remaining != None:
            children_init_hunger_percent = self.genome.gestation_period.value
            num_children : int = round(self.config.Evolution.max_children * self.genome.fecundity.value)
            children : list[Entity] = []
            for _ in range(num_children):
                new_genome = self.genome.combine(self.other_parent_genome, True, 5)
                initial_hunger = children_init_hunger_percent * -sin(pi * new_genome.speed.value - (pi/2)) + 1
                children.append(Entity(
                    specie=self.specie,
                    genome=new_genome,
                    hunger=initial_hunger,
                    cur_day=cur_time,
                    config=self.config,
                ))
            self.other_parent_genome = None
            self.pregnant_remaining = None
            return children
        else:
            raise ValueError(f"Either 'other_parent_genome' [{self.other_parent_genome}] or 'pregnant_remaining' [{self.pregnant_remaining}] are 'None'!")

    def is_mate_compatible(self, entity : "Entity") -> bool:
        if self.is_male() != entity.is_male(): # Test if opposite gender.
            if not entity.is_male() and not entity.is_pregnant(): # If target is female and not pregnant.
                return True
        return False

    def age(self, current_day : int) -> float:
        return current_day - self.__day_born
    
    def kill(self) -> None:
        self.__is_alive = False
    
    def is_male(self) -> bool:
        return self.genome.gender == Common.Genomes.Gender.MALE
    
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
    def day_born(self) -> float:
        return self.__day_born

    @property
    def is_alive(self) -> bool:
        return self.__is_alive

    def is_pregnant(self) -> bool:
        return self.other_parent_genome != None and self.pregnant_remaining != None

    def __repr__(self) -> str:
        return f"Entity; uuid:{str(self.__uuid)}"
    
    def __hash__(self) -> int:
        return hash(str(self.__uuid))