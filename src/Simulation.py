import board
import random

from entities import Entity
from Common import Species, Genomes, calc_distance


def create_new_board(size: tuple[int, int], entities: dict[Species.BaseSpecie, int]) -> board.Board:
    width, height = size
    new_board = board.Board(width, height, 5)

    for target_species, num in zip(entities.keys(), entities.values()):
        for _ in range(num):
            new_board.set_entity(
                entity=Entity(
                    specie=target_species,
                    genome=Genomes.Genome(
                        speed_gene=Genomes.Gene("speed", 0.5, 0.2),
                        hunger_rate_gene=Genomes.Gene("hunger_rate", 0.5, 0.2),
                        max_hunger_gene=Genomes.Gene("max_hunger", 0.5, 0.2),
                        vision_range_gene=Genomes.Gene("vision_range", 0.5, 0.2),
                        gestation_period_gene=Genomes.Gene(
                            "gestation_period", 0.5, 0.2
                        ),
                    ),
                    cur_day=0,
                ),
                location=(
                    random.randint(0, new_board.max_x_coord),
                    random.randint(0, new_board.max_x_coord),
                ),
            )
    return new_board


class Simulation:
    entity_board: board.Board

    time_created: float
    time_delta: float
    global_time: float

    def __init__(self, entity_board: board.Board, cur_time: float, time_delta: float) -> None:
        self.entity_board = entity_board
        self.time_created = cur_time
        self.time_delta = time_delta

    def adjust_time_delta(self, new_td: float) -> None:
        self.time_delta = new_td

    def run(self, num_steps: int) -> None:
        for _ in range(num_steps):
            # TODO Phase 1
            # First loop should let all of the entities on the board observe.
            # Entities in this phase should also do a risk assesment of every action.
            # All observations and risk assesments should be output to the log using Log Level DATA.
            for entity in self.entity_board.all_entities:
                if (entity.specie.can_see):  # If an entity cannot see, then it cannot do any actions anyway.
                    # Update entities memory
                    entity.memory.update()
                    
                    # Get entities surroundings and some basic context
                    cur_x, cur_y = self.entity_board.get_entity_location(entity)
                    observation = self.entity_board.get_all_in_view(entity)
                    identified = entity.identify_multiple_relationships(list(observation.keys()))
                    distances = {target: calc_distance(x, y, cur_x, cur_y) for target, x, y in observation.items()}
                    
                    # Log predators in current entities memory.
                    for predator, x, y in identified[Species.SpecieRelationship.PREDATOR]:
                        entity.memory.remember_entity_location(predator, x, y)
                    
                    for _, x, y in identified[Species.SpecieRelationship.PREY]:
                        entity.memory.remember_food_location(x, y)
                    
                    # This section has to do with predators, and how they move.
                    ...

            # TODO Phase 2
            # Second loop should let every entity decide what action to commit.
            # The actions are then done.
            # The new position and commited actions should be output to the log using Log Level DATA.
            for entity in self.entity_board.entities:
                ...

            self.global_time += self.time_delta
