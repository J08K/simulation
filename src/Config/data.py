class SimulationConfig:
    
    max_agents : int
    start_agents : int
    time_delta : float
    num_steps : int

    def __init__(
                self, 
                max_agents : int,
                start_agents : int, 
                time_delta : float,
                num_steps : int
            ) -> None:
        self.max_agents = max_agents
        self.start_agents = start_agents
        self.time_delta = time_delta
        self.num_steps = num_steps
        
    def export(self) -> dict:
        return {
            "max_agents": self.max_agents,
            "start_agents": self.start_agents,
            "time_delta": self.time_delta,
            "num_steps": self.num_steps,
        }
    
    @staticmethod
    def from_dict(obj : dict) -> "SimulationConfig":
        # TODO Error handling for missing data.
        return SimulationConfig(
            max_agents=obj["max_agents"],
            start_agents=obj["start_agents"],
            time_delta=obj["time_delta"],
            num_steps=obj["num_steps"],
        )
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