import random
import enum
from typing import Any

from uuid import UUID, uuid4

def calc_mutation(value : float, mutability : float, accuracy : int) -> float:
    div = 10 ** accuracy
    max_change = int(mutability * div)
    change = random.randrange( -max_change, max_change, 1) / div
    return round(value * (1 + change), accuracy)


class Gender(enum.Enum):
    # Controversial, but for simplicity only having 2 genders. :)
    MALE = 0
    FEMALE = 1


class Gene:

    name : str
    value : float
    mutability : float

    __uuid : UUID

    def __init__(self, name : str, start_value : float, mutability : float) -> None:
        self.name = name
        self.value = start_value 
        self.mutability = mutability
        
        self.__uuid = uuid4()
        
    def combine(self, other : "Gene", do_mutate : bool, accuracy : int) -> "Gene":
        if self.name != other.name:
            raise ValueError(f"Gene names are not the same: ({self.name} <> {other.name})!")

        new_value = (self.value + other.value) / 2
        new_mutability = (self.mutability + other.mutability) / 2
        
        if do_mutate:
            new_value = calc_mutation(new_value, new_mutability, accuracy)
            new_mutability = calc_mutation(new_mutability, new_mutability, accuracy)

        new_gene = Gene(
            name=self.name,
            start_value=new_value,
            mutability=new_mutability,
        )
        
        return new_gene

    def export_dict(self) -> dict[str, float | str]:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "value": self.value,
            "mutability": self.mutability,
        }

    @property
    def uuid(self) -> str:
        return str(self.__uuid)


class Genome:
    
    # TODO Might want to add memory length.
    
    speed : Gene
    vision_range : Gene
    gestation_period : Gene
    fecundity: Gene
    
    gender : Gender
    
    __uuid : UUID
    
    def __init__(self, 
                 speed_gene : Gene, 
                 vision_range_gene : Gene,
                 gestation_period_gene : Gene, 
                 fecundity: Gene, # https://www.khanacademy.org/science/ap-biology/ecology-ap/energy-flow-through-ecosystems/a/life-history-strategies
                 gender : Gender
                 ) -> None:
        self.speed = speed_gene
        self.vision_range = vision_range_gene
        self.gestation_period = gestation_period_gene
        self.fecundity = fecundity
        self.gender = gender
        
        self.__uuid = uuid4()
        
    def combine(self, other : "Genome", do_mutate : bool, accuracy : int) -> "Genome":
        new_speed = self.speed.combine(other.speed, do_mutate, accuracy)
        new_vision_range = self.vision_range.combine(other.vision_range, do_mutate, accuracy)

        new_gestation_period = self.gestation_period.combine(other.gestation_period, do_mutate, accuracy)
        new_fecundity = self.fecundity.combine(other.fecundity, do_mutate, accuracy)
        
        new_gender = random.choice([Gender.FEMALE, Gender.MALE]) # TODO Research if there are other factors affecting gender.
        
        new_genome = Genome(
            speed_gene=new_speed,
            vision_range_gene=new_vision_range,
            gestation_period_gene=new_gestation_period,
            fecundity=new_fecundity,
            gender=new_gender
        )
        
        return new_genome
        
    @property
    def uuid(self) -> str:
        return str(self.__uuid)
    
    def export_dict(self) -> dict[str, Any]:
        return {
            "uuid": self.uuid,
            "gender": self.gender.name,
            "genes": [
                self.speed.export_dict(),
                self.vision_range.export_dict(),
                self.gestation_period.export_dict(),
                self.fecundity.export_dict(),
            ]    
        }
        