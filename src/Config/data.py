from typing import Any


class BaseConf:

    def __init__(self) -> None:
        pass

    def export(self) -> dict:
        keys = [idx for idx in dir(self) if not idx.endswith("__")]
        return {key:self.__getattribute__(key) for key in keys}

class SimulationConfig(BaseConf):
    
    width : float
    height : float
    grid_size : float
    time_delta : float
    num_steps : float

    def __init__(self, 
                width : float,
                height : float,
                grid_size : float,
                time_delta : float,
                num_steps : float,
            ) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.time_delta = time_delta
        self.num_steps = num_steps


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

    mutability : str

    def __init__(self, mutability : str) -> None:
        super().__init__()
        self.mutability = mutability


class SpeciesConfig(BaseConf):

    species : dict[str, dict[str, Any]]

    def __init__(self, species: dict[str, dict[str, Any]]) -> None:
        super().__init__()
        self.species = species

class Config:
    
    Simulation : SimulationConfig
    
    def __init__(self, sim_conf : SimulationConfig) -> None:
        self.Simulation = sim_conf
        
    def export(self) -> dict:
        return {
            "simulation": self.Simulation.export(),
        }

    @staticmethod
    def from_dict(obj : dict) -> "Config":
        # TODO Add error handling for missing config points.
        new_conf = dict()
        
        for conf_title, data in obj.items():
            match str(conf_title).lower():
                case "simulation":
                    new_conf["simulation"] = SimulationConfig.from_dict(data)
        
        new_conf_obj = Config(
            sim_conf=new_conf["simulation"],
        )
        
        return new_conf_obj