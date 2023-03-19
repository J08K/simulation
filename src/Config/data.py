from typing import Any
from Common import Species

class BaseConf:

    def __init__(self) -> None:
        pass

    def export(self) -> dict[str, Any]:
        keys = [idx for idx in dir(self) if not idx.endswith("__")]
        return {key:self.__getattribute__(key) for key in keys}

class SimulationConfig(BaseConf):
    
    width : float
    height : float
    grid_size : float
    time_delta : float
    num_steps : int
    static_entity_spawn_rate: int
    static_entity_spawn_interval: int

    def __init__(self, 
                width : float,
                height : float,
                grid_size : float,
                time_delta : float,
                num_steps : int,
                static_entity_spawn_rate: int,
                static_entity_spawn_interval: int,
            ) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.time_delta = time_delta
        self.num_steps = num_steps
        self.static_entity_spawn_rate = static_entity_spawn_rate
        self.static_entity_spawn_interval = static_entity_spawn_interval


class LoggerConfig(BaseConf):

    db_uri : str
    db_port : int
    db_username : str
    db_password : str
    db_collection_name : str

    def __init__(self,
                db_uri : str,
                db_port : int,
                db_username : str,
                db_password : str,
                db_collection_name : str,
                 ) -> None:
        super().__init__()
        self.db_uri = db_uri
        self.db_port = db_port
        self.db_username = db_username
        self.db_password = db_password
        self.db_collection_name = db_collection_name


class EvolutionConfig(BaseConf):

    mutability : float
    max_children : int

    def __init__(self, mutability: float, max_children: int) -> None:
        super().__init__()
        self.mutability = mutability
        self.max_children = max_children


class EntitiesConfig(BaseConf):

    hunger_speed_multiplier: float
    short_term_memory_span: float
    long_term_memory_span: float
    prey_saturation: float

    def __init__(self, hunger_speed_multiplier : float, short_term_memory_span : float, long_term_memory_span : float, prey_saturation: float) -> None:
        super().__init__()
        self.hunger_speed_multiplier = hunger_speed_multiplier
        self.short_term_memory_span = short_term_memory_span
        self.long_term_memory_span = long_term_memory_span
        self.prey_saturation = prey_saturation
        

class SpeciesConfig(BaseConf):

    species : dict[Species.BaseSpecie, int]

    def __init__(self, species: dict[str, dict[str, Any]]) -> None:
        super().__init__()
        self.species = {Species.BaseSpecie(val["id"], idx, val["prey"], val["can_move"], val["can_see"]): val["start_amount"] for idx, val in species.items()}

    def items(self) -> list[tuple[Species.BaseSpecie, int]]:
        return list(self.species.items())

class Config:
    
    Simulation: SimulationConfig
    Logger: LoggerConfig
    Evolution: EvolutionConfig
    Entities: EntitiesConfig
    Species: SpeciesConfig
    
    def __init__(self, sim_conf: SimulationConfig, log_conf: LoggerConfig, evo_conf: EvolutionConfig, ent_conf: EntitiesConfig, spe_conf: SpeciesConfig) -> None:
        self.Simulation = sim_conf
        self.Logger = log_conf
        self.Evolution = evo_conf
        self.Entities = ent_conf
        self.Species = spe_conf
        
    def export(self) -> dict[str, dict[str, Any]]:
        return { # TODO Export it in a way that it would be easily parsed to the TOML config format.
            "simulation": self.Simulation.export(),
            "logger": self.Logger.export(),
            "evolution": self.Evolution.export(),
            "entities": self.Entities.export(),
            "species": self.Species.export(),
        }