# Module responsible for entity memory

from uuid import UUID

class Memory:
    
    memory_len : float
    
    times : dict[
                float, 
                dict[
                    str, 
                    dict[
                        UUID, 
                        tuple[float, float]]
                    ]
                ] # Store an entities location by date.
    
    def __init__(self, memory_len : float) -> None:
        self.memory_len = 0.0
        self.entity_locations = dict()
    
    def update(self, current_time : float) -> None:
        # * This function has to be run before memory is accessed each step.
        
        # Delete old information
        for stored_time in self.times.keys():
            if current_time - self.memory_len > stored_time:
                self.times.pop(stored_time)
        ...