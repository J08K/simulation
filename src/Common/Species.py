import enum


class SpecieRelationship(enum.Enum):
    """Enum for different types of relationships between species.

    Defines the relationship of a specie with that of another specie.
    
    This is from the view of the current specie.
    
    e.g: The current specie _sees_ a "predator".
    """
    
    PREDATOR = 0
    NEUTRAL = 1
    PREY = 2
    CONGENER = 3


class BaseSpecie:
    
    __name : str
    __id : int
    __edible_entities : list[int]
    
    def __init__(self, id : int, name : str, prey : list[int]) -> None:
        self.__id = id
        self.__name = name
        self.__edible_entities = prey
    
    def identify_relationship(self, entity_specie : "BaseSpecie") -> SpecieRelationship:
        if self.id in entity_specie.prey:
            return SpecieRelationship.PREDATOR
        elif entity_specie.id in self.__edible_entities:
            return SpecieRelationship.PREY
        elif entity_specie.id == self.id:
            return SpecieRelationship.CONGENER
        else:
            return SpecieRelationship.NEUTRAL
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def prey(self) -> list[int]:
        return self.__edible_entities