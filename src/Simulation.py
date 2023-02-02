import board
import random

from entities import Entity
from Common import Species, Genomes


def create_new_board(size : tuple[int, int], entities : dict[Species.BaseSpecie, int]) -> board.Board:
    width, height = size
    new_board = board.Board(width, height)
    
    for target_species, num in zip(entities.keys(), entities.values()):
        for _ in range(num):
            new_board.set_entity(entity=Entity(
                specie=target_species,
                genome=Genomes.Genome(
                    speed_gene=Genomes.Gene("speed", 0.5, 0.2),
                    hunger_rate_gene=Genomes.Gene("hunger_rate", 0.5, 0.2),
                    max_hunger_gene=Genomes.Gene("max_hunger", 0.5, 0.2),
                    vision_range_gene=Genomes.Gene("vision_range", 0.5, 0.2),
                    gestation_period_gene=Genomes.Gene("gestation_period", 0.5, 0.2),
                ),
                cur_day=0,
            ), location=(
                random.randint(0, new_board.max_x_coord), 
                random.randint(0, new_board.max_x_coord)
            ))
    return new_board

class Simulation:
    
    entity_board : board.Board
    
    time_created : float
    time_delta : float
    global_time : float
    
    def __init__(self, entity_board : board.Board, cur_time : float, time_delta : float) -> None:
        self.entity_board = entity_board
        self.time_created = cur_time
        self.time_delta = time_delta
    
    def adjust_time_delta(self, new_td : float) -> None:
        self.time_delta = new_td
    
    def run(self, num_steps : int) -> None:
        for _ in range(num_steps):
            # TODO Phase 1
            # First loop should let all of the entities on the board observe.
            # Entities in this phase should also do a risk assesment of every action.
            # All observations and risk assesments should be output to the log using Log Level DATA.
            for entity in self.entity_board.entities:
                ...
            
            # TODO Phase 2
            # Second loop should let every entity decide what action to commit.
            # The actions are then done.
            # The new position and commited actions should be output to the log using Log Level DATA.
            for entity in self.entity_board.entities:
                ...
            
            self.global_time += self.time_delta