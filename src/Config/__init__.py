import os
import pathlib
import toml
from Config import data as ConfigData
from Config import defaults as ConfigDefaults

__version__ = "0.0.1"

PROJECT_OWNER = "J08K"
PROJECT_NAME = "PWS"

def get_default_config_dir() -> pathlib.Path:
    return pathlib.Path(f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\{PROJECT_OWNER}\\{PROJECT_NAME}")

class NoWritePermission(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args) # TODO Add some stuff to this, so that it makes sense for this exception class to be here.

class ProjectConfigHandler:
    
    PROJECT_OWNER = PROJECT_OWNER
    PROJECT_NAME = PROJECT_NAME
    
    config_root : pathlib.Path
    config_file_path : pathlib.Path
    
    # * Config data
    config : ConfigData.Config
    
    def __init__(self, config_path : str = "") -> None:
        self.config = None
        
        if config_path:
            self.config_root = config_path
        else:
            self.config_root = get_default_config_dir()
            self.config_file_path = self.config_root / "config.toml"

        if "config.toml" in os.listdir():
            self.config_file_path = pathlib.Path(os.path.abspath(os.getcwd())) / "config.toml"

        self.integrity_check()
        self.read_config()
    
    def read_config(self) -> None:
        with open(self.config_file_path, "r") as config_file:
            data = toml.load(config_file)
            self.config = ConfigData.Config( # TODO This is awful, not everything has to be class and object based.
                # Prime example of why people hate OOP, this... (Job Kolhorn, 2023)
                sim_conf=ConfigData.SimulationConfig(
                    width=data["simulation"]["width"],
                    height=data["simulation"]["height"],
                    grid_size=data["simulation"]["grid_size"],
                    time_delta=data["simulation"]["time_delta"],
                    num_steps=data["simulation"]["num_steps"],
                ),
                log_conf=ConfigData.LoggerConfig(
                    db_uri=data["logger"]["db"]["uri"],
                    db_port=data["logger"]["db"]["port"],
                    db_username=data["logger"]["db"]["username"],
                    db_password=data["logger"]["db"]["password"],
                    db_collection_name=data["logger"]["db"]["collection_name"],
                ),
                evo_conf=ConfigData.EvolutionConfig(
                    mutability=data["evolution"]["mutability"],
                    max_children=data["evolution"]["max_children"],
                ),
                ent_conf=ConfigData.EntitiesConfig(
                    hunger_speed_multiplier=data["entities"]["hunger_speed_multiplier"],
                    short_term_memory_span=data["entities"]["short_term_memory_span"],
                    long_term_memory_span=data["entities"]["long_term_memory_span"],
                    prey_saturation=data["entities"]["prey_saturation"],
                ),
                spe_conf=ConfigData.SpeciesConfig(
                    species=data["species"]
                )
            )

    def integrity_check(self) -> None:
        if not os.access(self.config_root.parent.parent, os.W_OK): # Check if the process has write access to the directory.
            raise NoWritePermission("Directory: ")
        if not os.path.isdir(self.config_root.parent): # Check if the PROJECT_OWNER directory exists.
            os.mkdir(self.config_root.parent)
        if not os.path.isdir(self.config_root): # Check if the PROJECT_NAME folder exists.
            os.mkdir(self.config_root)
        if not os.path.exists(self.config_file_path): # Check if the main config file exists.
            ConfigDefaults.genDefaultConfig(self.config_file_path)
        
    def export(self) -> dict:
        return {
            "project_owner": self.PROJECT_OWNER,
            "project_name": self.PROJECT_NAME,
            "dir_path": self.config_root,
            "file_path": self.config_file_path,
            "config": self.config.export(),
        }
    
    def get_config_dir(self) -> pathlib.Path:
        return self.config_root
    
