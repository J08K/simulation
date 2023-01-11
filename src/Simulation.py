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
    
    time : float
    time_delta : float
    
    def __init__(self, entity_board : board.Board, cur_time : float, time_delta : float) -> None:
        self.entity_board = entity_board
        self.time = cur_time
        self.time_delta = time_delta
    
    def adjust_time_delta(self, new_td : float) -> None:
        self.time_delta = new_td
    
    def run(self, num_cycles : int) -> None:
        for cycle_idx in range(num_cycles):
            
            for entity in self.entity_board.entities:
                ...
            
            
            self.time += self.time_delta