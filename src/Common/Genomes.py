import random
import enum

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

    def export_dict(self) -> dict:
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
    hunger_rate : Gene
    max_hunger : Gene
    vision_range : Gene
    gestation_period : Gene
    
    gender : Gender
    
    __uuid : UUID
    
    def __init__(self, 
                 speed_gene : Gene, 
                 hunger_rate_gene : Gene, 
                 max_hunger_gene : Gene,
                 vision_range_gene : Gene,
                 gestation_period_gene : Gene,
                 gender : Gender
                 ) -> None:
        self.speed = speed_gene
        self.hunger_rate = hunger_rate_gene
        self.max_hunger = max_hunger_gene
        self.vision_range = vision_range_gene
        self.gestation_period = gestation_period_gene
        self.gender = gender
        
        self.__uuid = uuid4()
        
    def combine(self, other : "Genome", do_mutate : bool, accuracy : int) -> "Genome":
        new_speed = self.speed.combine(other.speed, do_mutate, accuracy)
        new_hunger_rate = self.hunger_rate.combine(other.hunger_rate, do_mutate, accuracy)
        new_max_hunger = self.max_hunger.combine(other.max_hunger, do_mutate, accuracy)
        new_vision_range = self.vision_range.combine(other.vision_range, do_mutate, accuracy)

        new_gestation_period = self.gestation_period.combine(other.gestation_period, do_mutate, accuracy)
        
        new_gender = random.choice([Gender.FEMALE, Gender.MALE]) # TODO Research if there are other factors affecting gender.
        
        new_genome = Genome(
            speed_gene=new_speed,
            hunger_rate_gene=new_hunger_rate,
            max_hunger_gene=new_max_hunger,
            vision_range_gene=new_vision_range,
            gestation_period_gene=new_gestation_period,
            gender=new_gender
        )
        
        return new_genome
        
    @property
    def uuid(self) -> str:
        return str(self.__uuid)
    
    def export_dict(self) -> dict:
        return {
            "uuid": self.uuid,
            "gender": self.gender.name,
            "genes": {
                "speed": self.speed.export_dict(),
                "hunger_rate": self.hunger_rate.export_dict(),
                "max_hunger": self.max_hunger.export_dict(),
                "vision_range": self.vision_range.export_dict(),
                "gestation_period": self.gestation_period.export_dict(),
            }
        }
        