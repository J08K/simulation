import os
import pathlib
import toml # TODO ADD TOML import
from Config import data as ConfigData
from Config import defaults as ConfigDefaults

__version__ = "0.0.1"

class NoWritePermission(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args) # TODO Add some stuff to this, so that it makes sense for this exception class to be here.

class ProjectConfigHandler:
    
    PROJECT_OWNER = "J08K"
    PROJECT_NAME = "PWS"
    
    config_root : pathlib.Path
    config_file_path : pathlib.Path
    
    # * Config data
    config : ConfigData.Config
    
    def __init__(self, config_path : str = "") -> None:
        self.config = None
        
        if config_path == "":
            self.config_root = pathlib.Path(f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\{self.PROJECT_OWNER}\\{self.PROJECT_NAME}")
        else:
            self.config_root = config_path   
        self.config_file_path = self.config_root / "config.toml"
        self.integrity_check()
        self.read_config()
    
    def read_config(self) -> None:
        with open(self.config_file_path, "r") as config_file:
            data = toml.load(config_file)
            self.config = ConfigData.Config.from_dict(data)
    
    def create_default_config(self, config_path : pathlib.Path) -> None:
        default_config = ConfigDefaults.DEFAULT_CONFIG
        with open(config_path, "w+") as config_fp:
            toml.dump(default_config.export(), config_fp)
    
    def integrity_check(self) -> None:
        if not os.access(self.config_root.parent.parent, os.W_OK):
            raise NoWritePermission("Directory: ")
        if not os.path.isdir(self.config_root.parent):
            os.mkdir(self.config_root.parent)
        if not os.path.isdir(self.config_root):
            os.mkdir(self.config_root)
        if not os.path.exists(self.config_file_path):
            self.create_default_config(self.config_file_path)
        
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
    
