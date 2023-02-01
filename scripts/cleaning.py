import os
import pathlib

PROJECT_OWNER = "J08K"
PROJECT_NAME = "PWS"

def delete_content(dir : pathlib.Path) -> None:
    for item in os.listdir(dir):
        path = dir / pathlib.Path(item)
        if os.path.isdir(path):
            delete_content(path)
            os.rmdir(path)
            print(f"[REMOVED]: {path}")
        else:
            try:
                os.remove(path)
                print(f"[REMOVED]: {path}")
            except FileNotFoundError:
                print(f"Could not find file: {path.absolute()}")

def clean_pycache(dir : pathlib.Path) -> None:
    dir = pathlib.Path(dir)
    for item in os.listdir(dir):
        path = dir / pathlib.Path(item)
        if os.path.isdir(path):
            if item == "__pycache__":
                delete_content(path)
                os.rmdir(path)
                print(f"[REMOVED]: {path}")
            else:
                clean_pycache(path)

def clean_config() -> None:
    config_path = pathlib.Path(f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\{PROJECT_OWNER}\\{PROJECT_NAME}")
    if os.path.exists(config_path):
        print("[CONFIG]: Found config directory! Deleting...")
        delete_content(config_path)
        os.rmdir(config_path)
    else:
        print("[CONFIG]: Did not find a config directory.")
    
if __name__ == "__main__":
    print("[PYCACHE]: Cleaning pycache...")
    clean_pycache(os.curdir)
    print("[PYCACHE]: Done cleaning pycache!")
    
    clean_config()