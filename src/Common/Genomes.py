import random
import math

from uuid import UUID, uuid4

def calc_mutation(value : float, mutability : float, accuracy : int) -> float:
    div = 10 ** accuracy
    max_change = int(mutability * div)
    change = random.randrange( -max_change, max_change, 1) / div
    return round(value * (1 + change), accuracy)
    
class Gene:

    name : str
    value : float
    mutability : float
    accuracy : float
    
    __uuid : UUID
    
    def __init__(self, name : str, start_value : float, mutability : float, accuracy : int = 3) -> None:
        self.name = name
        self.value = start_value
        self.mutability = mutability
        self.accuracy = accuracy
        
        self.__uuid = uuid4()
        
    def combine_genes(self, other : "Gene", do_mutate : bool) -> "Gene":
        if self.name != other.name:
            raise ValueError(f"Gene names are not the same: ({self.name} <> {other.name})!")
        avg_value = (self.value + other.value) / 2
        avg_mutability = (self.mutability + other.mutability) / 2
        avg_accuracy = math.ceil((self.accuracy + other.accuracy) / 2)
        return avg_value if not do_mutate else calc_mutation(avg_value, avg_mutability, avg_accuracy)
        

    @property
    def uuid(self) -> str:
        return str(self.__uuid)
    
    def __dict__(self) -> dict:
        return {
            "type" : "Gene",
            "uuid" : self.uuid,
            "data" : {
                "name" : self.name,
                "value" : self.value,
                "mutability" : self.mutability,
                "accuracy" : self.accuracy
            }
        }

class Genome:
    ...
    
print(calc_mutation(1.0, 0.1, 5))