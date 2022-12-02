import board

class Simulation:
    
    entity_board : board.Board
    
    time : float
    time_delta : float
    
    def __init__(self, entity_board : board.Board, cur_time : float, time_delta : float) -> None:
        self.entity_board = entity_board
        self.time = cur_time
        self.time_delta = time_delta
        
    def run(self, num_cycles : int):
        for cycle_idx in range(num_cycles):
            
            for entity in self.entity_board.entities:
                ...
            
            
            self.time += self.time_delta