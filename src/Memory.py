# Module responsible for entity memory

from uuid import UUID

class ShortTermMemory:

    entity_locations : dict[UUID, tuple[float, tuple[float, float]]] # Store entity locations.
    memory_length : float # How long data in the short term memory will last.

    def __init__(self, memory_len : float) -> None:
        self.entity_locations = dict()
        self.memory_length = memory_len

    def update(self, current_time) -> None:
        for entity, (time_stamp, _) in self.entity_locations.items():
            if current_time - time_stamp > self.memory_length:
                self.entity_locations.pop(entity)

    def add_entity(self, entity_uuid: UUID, x: float, y: float, timestamp : float) -> None:
        self.entity_locations[entity_uuid] = (timestamp, (x, y))

    def get_entities(self) -> list[tuple[UUID, tuple[float, float]]]:
        return [(uuid, location) for uuid, (_, location) in self.entity_locations.items()]

    def export_dict(self) -> dict:
        return {
            "memory_length": self.memory_length,
            "entity_locations": [{
                "uuid": str(uuid),
                "time_added": timestamp,
                "x": x,
                "y": y,
            } for uuid, (timestamp, (x, y)) in self.entity_locations.items()]
        }

class LongTermMemory:

    # Store location of food seen.
    static_food_locations : list[tuple[float, tuple[float, float]]]
    memory_length : float

    def __init__(self, memory_length: float) -> None:
        self.static_food_locations = []
        self.memory_length = memory_length

    def update(self, current_time: float) -> None:
        for idx, (timestamp, _) in enumerate(self.static_food_locations):
            if current_time - timestamp > self.memory_length:
                self.static_food_locations.pop(idx)

    def add_food(self, x: float, y: float, timestamp: float) -> None:
        self.static_food_locations.append((timestamp, (x, y)))

    def export_dict(self) -> dict:
        return {
            "memory_length": self.memory_length,
            "static_food_locations": [{
                "time_added": timestamp,
                "x": x,
                "y": y,
            } for timestamp, (x, y) in self.static_food_locations]
        }
class Memory:

    # TODO Make sure this object is correctly implemented in species.

    long_term : LongTermMemory
    short_term : ShortTermMemory
    
    current_time : float
    
    def __init__(self, long_term_length : float, short_term_length : float, current_time : float) -> None:
        self.short_term = ShortTermMemory(short_term_length)
        self.long_term = LongTermMemory(long_term_length)
        self.current_time = current_time
    
    def update(self, current_time : float) -> None:
        """
        This function has to be run before memory is accessed each step.
        """

        self.current_time = current_time
        self.short_term.update(current_time)
        self.long_term.update(current_time)
        
    
    def remember_entity_location(self, entity_uuid : UUID, x: float, y: float) -> None:
        self.short_term.add_entity(entity_uuid, x, y, self.current_time)


    def remember_food_location(self, x: float, y: float) -> None:
        self.long_term.add_food(x, y, self.current_time)


    def export_dict(self) -> dict:
        return {
            "current_time": self.current_time,
            "long_term": self.long_term.export_dict(),
            "short_term": self.short_term.export_dict(),
        }