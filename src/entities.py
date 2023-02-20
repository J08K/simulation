from uuid import UUID, uuid4

import Common
import vision
import Memory

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

    # Metadata
    __uuid : UUID
    
    def __init__(self, specie: Common.Species.BaseSpecie, genome : Common.Genomes.Genome, cur_day : int) -> None:
        self.specie = specie
        self.genome = genome

        self.eyes = vision.Vision(self.genome.vision_range.value)
        self.memory = Memory.Memory(3.0, 5.0, cur_day) # TODO Add NON arbitrary values.

        self.__is_alive = True
        self.__day_born = cur_day # TODO Convert to timestamp of global time, when born.

        self.__uuid = uuid4()
    
    def do_action(self, cur_location : tuple[float, float], surroundings : dict["Entity", tuple[float, float]]):
        ...
    
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