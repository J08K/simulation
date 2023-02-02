# Module responsible for entity memory

from uuid import UUID

class ShortTermMemory:

    entity_locations : dict[UUID, tuple[float, float]] # Store entity locations.

    def __init__(self) -> None:
        self.entity_locations = dict()

    def add_entity(self, entity_uuid : UUID, location : tuple[float, float]) -> None:
        self.entity_locations[entity_uuid] = location

class LongTermMemory:

    # Store location of food seen.
    # TODO Make it so that you can also hash for food by location.
    static_food_locations : list[tuple[float, float]]

    def __init__(self) -> None:
        self.static_food_locations = []

    def add_food(self, location : tuple[float, float]) -> None:
        self.static_food_locations.append(location)

class Memory:
    
    memory_len : float
    
    __current_time : float

    register : dict[float, list[ShortTermMemory, LongTermMemory]]
    
    def __init__(self, memory_len : float) -> None:
        self.memory_len = memory_len
        self.times = dict()
    
    def update(self, current_time : float) -> None:
        """
        This function has to be run before memory is accessed each step.
        """

        self.__current_time = current_time

        # Delete old information
        for stored_time in self.times.keys():
            if self.__current_time - self.memory_len > stored_time:
                self.times.pop(stored_time)

        # Add current time
        self.__add_current_time()
        

    def __add_current_time(self) -> None:
        if self.__current_time not in self.times:
            self.register[self.__current_time] = [ShortTermMemory(), LongTermMemory()]

    def remember_entity_location(self, entity_uuid : UUID, location : tuple[float, float]) -> None:
        self.register[self.__current_time][0].add_entity(entity_uuid, location)

    def remember_food_location(self, location : tuple[float, float]) -> None:
        self.register[self.__current_time][1].add_food(location)