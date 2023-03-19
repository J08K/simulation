import board
import random

from entities import Entity
from Common import Species, Genomes, calc_distance, clamp
from move import Direction

from Config import ConfigData

def create_new_board(config : ConfigData.Config) -> board.Board:
    new_board = board.Board(config.Simulation.width, config.Simulation.height, config.Simulation.grid_size)

    for specie, num in config.Species.items():
        mut = config.Evolution.mutability
        for _ in range(num):
            new_board.add_entity(
                entity=Entity(
                    config=config,
                    specie=specie,
                    genome=Genomes.Genome(
                        speed_gene=Genomes.Gene("speed", 0.5, mut),
                        vision_range_gene=Genomes.Gene("vision_range", 0.5, mut),
                        gestation_period_gene=Genomes.Gene("gestation_period", 0.5, mut),
                        fecundity=Genomes.Gene("fecundity", 0.5, mut),
                        gender=random.choice([Genomes.Gender.FEMALE, Genomes.Gender.MALE])
                    ),
                    hunger=0.0,
                    cur_day=0,
                ),
                x=random.random() * new_board.max_x_coord,
                y=random.random() * new_board.max_y_coord,
            )
    return new_board


class Simulation:
    entity_board: board.Board

    time_created: float
    time_delta: float
    global_time: float
    
    config : ConfigData.Config
    # TODO This should implement a logger.

    def __init__(self, entity_board: board.Board, config : ConfigData.Config) -> None:
        self.config = config

        self.entity_board = entity_board
        self.time_created = 0.0
        self.time_delta = self.config.Simulation.time_delta
        self.global_time = 0.0

    def adjust_time_delta(self, new_td: float) -> None:
        self.time_delta = new_td

    def export_dict(self) -> dict:
        return {
            "time_zero" : self.time_created,
            "time_delta" : self.time_delta,
            "time_current" : round(self.global_time, len(str(self.time_delta)[2:])),
            "board": self.entity_board.export_dict()
        }

    def step(self) -> None:

        ENTITY_REF_SPEED = 8 # * In meters per second

        # First loop should let all of the entities on the board observe.
        # Entities in this phase should also do a risk assesment of every action.
        # All observations and risk assesments should be output to the log using Log Level DATA.
        for current_entity in self.entity_board.all_entities:
            if current_entity.specie.can_see and current_entity in self.entity_board:  # If an entity cannot see, then it cannot do any actions anyway.
                # TODO Update entities memory
                # current_entity.memory.update()
                
                # ///////////////////////////////////////////////////////////////////
                # Get entity context
                entity_speed = ENTITY_REF_SPEED * current_entity.genome.speed.value
                max_travel_distance = self.time_delta * entity_speed
                
                hunger_used = self.config.Entities.hunger_speed_multiplier
                if current_entity.hunger + self.config.Entities.hunger_speed_multiplier >= current_entity.max_hunger:
                    # TODO max_travel_distance should not be zero.
                    max_travel_distance = max_travel_distance * ((current_entity.max_hunger - current_entity.hunger) / self.config.Entities.hunger_speed_multiplier)
                    hunger_used = current_entity.max_hunger - current_entity.hunger

                # ///////////////////////////////////////////////////////////////////
                # Get entities surroundings
                cur_x, cur_y = self.entity_board.get_entity_location(current_entity)
                observation = self.entity_board.get_all_in_view(current_entity)
                identified = current_entity.identify_multiple_relationships(list(observation.keys()))
                
                new_location = cur_x, cur_y

                # ///////////////////////////////////////////////////////////////////
                # * Get important entity locations.

                food_location = None
                predator_location = None
                mate_location = None

                # Go to closest food if it exists.
                if identified[Species.SpecieRelationship.PREY]:
                    # Get closest food
                    closest_food = min(identified[Species.SpecieRelationship.PREY], key=lambda target: calc_distance(cur_x, cur_y, *self.entity_board.get_entity_location(target)))
                    food_location = self.entity_board.get_entity_location(closest_food)

                # Identify predators.
                if identified[Species.SpecieRelationship.PREDATOR]:
                    # Get closest predator
                    closest_predator = min(identified[Species.SpecieRelationship.PREDATOR], key=lambda target: calc_distance(cur_x, cur_y, *self.entity_board.get_entity_location(target)))
                    predator_location = self.entity_board.get_entity_location(closest_predator)
                
                if current_entity.is_male() or not (current_entity.is_male() and current_entity.is_pregnant()):
                    if identified[Species.SpecieRelationship.CONGENER]:
                        # Get closest mate
                                      
                
                # ///////////////////////////////////////////////////////////////////
                # Notes on decision making:
                
                # If an entity has a low hunger (i.e. 20% of max_hunger) then it should not be important to find food.
                
                # An entity should worry more about approaching predators than ones that aren't.
                
                # If an entity has a medium hunger (i.e. 60% of max_hunger) then it will prefer food in the opposite direction of a predator.
                
                # If an entity has a medium hunger (i.e. 60% of max_hunger) it will try to look for a compatible mate.
                
                # If an entity has a high hunger (i.e. ~85% of max_hunger) it will be highly focused on finding food.
                
                # ///////////////////////////////////////////////////////////////////
                # * Figure out where to move.

                if food_location or predator_location:
                    
                    # TODO Better decision making.

                    food_dist = None
                    if food_location:
                        food_dist = calc_distance(cur_x, cur_y, *food_location)
                    
                    predator_dist = None
                    if predator_location:
                        predator_dist = calc_distance(cur_x, cur_y, *predator_location)

                    if food_dist and (predator_dist == None or food_dist <= predator_dist):
                        # * Food is closest

                        diff_x, diff_y = Direction.max_delta_location(max_travel_distance, *Direction.calc_direction(cur_x, cur_y, *food_location))
                        new_location = cur_x + diff_x, cur_y + diff_y

                        if calc_distance(cur_x, cur_y, *food_location) <= max_travel_distance: # TODO Add max interaction range.
                            self.entity_board.kill_entity(closest_food)
                            current_entity.hunger -= self.config.Entities.prey_saturation
                        self.entity_board.set_entity_location(current_entity, *new_location)

                    else:
                        if predator_location:
                            # * Predator is closest
                            
                            diff_x, diff_y = Direction.max_delta_location(max_travel_distance, *Direction.calc_direction(cur_x, cur_y, *predator_location))
                            new_location = clamp(0, self.entity_board.max_x_coord, cur_x - diff_x), clamp(0, self.entity_board.max_y_coord, cur_y - diff_y) # Should go in the other direction of predator.

                            if random.randint(0, 9) != 0: # TODO Random failure due to stress, just so that entities can catch up.
                                self.entity_board.set_entity_location(current_entity, *new_location)


                else:
                    # Entity has not found a target and will move to a pseudo-random location.

                    if current_entity.fallback_location == None:
                        fallback_distance = max_travel_distance / self.time_delta * 5
                        direction = Direction.random_direction()
                        
                        diff_x, diff_y = Direction.max_delta_location(fallback_distance, *direction, True)
                        fall_x, fall_y = cur_x + diff_x, cur_y + diff_y
                        fall_x, fall_y = clamp(0, self.entity_board.max_x_coord, fall_x), clamp(0, self.entity_board.max_y_coord, fall_y)
                        
                        current_entity.fallback_location = fall_x, fall_y

                    fall_x, fall_y= current_entity.fallback_location

                    direction = Direction.calc_direction(cur_x, cur_y, fall_x, fall_y)

                    diff_x, diff_y = Direction.max_delta_location(max_travel_distance, *direction, True)
                    new_x, new_y = cur_x + diff_x, cur_y + diff_y
                    new_x, new_y = clamp(0, self.entity_board.max_x_coord, new_x), clamp(0, self.entity_board.max_y_coord, new_y)

                    self.entity_board.set_entity_location(current_entity, new_x, new_y)

                    if new_x == fall_x and new_y == fall_y:
                        current_entity.fallback_location = None

                # ///////////////////////////////////////////////////////////////////
                # Pregnancy
                
                # ! Technically entities should not be able to give birth if they have reached their maximum hunger, but whatever.
                if current_entity.is_pregnant():
                    current_entity.pregnant_remaining -= self.time_delta
                    if current_entity.pregnant_remaining <= 0:
                        children = current_entity.birth_children(self.global_time)
                        cur_x, cur_y = self.entity_board.get_entity_location(current_entity)
                        for child in children:
                            self.entity_board.add_entity(child, cur_x, cur_y)
                    else:
                        # Pregnant entities use more energy.
                        # TODO Add multiplier to config.
                        hunger_used += hunger_used * 1.5
                
                # ///////////////////////////////////////////////////////////////////
                
                current_entity.hunger += hunger_used
                if current_entity.hunger >= current_entity.max_hunger:
                    self.entity_board.kill_entity(current_entity)

        self.global_time += self.time_delta