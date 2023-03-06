import os
import pathlib
import sys

PROJECT_OWNER = "J08K"
PROJECT_NAME = "PWS"

def delete_content(dir : pathlib.Path, to_skip : list[str]) -> None:
    for item in os.listdir(dir):
        delete = True
        for skipped in to_skip:
            if item.endswith(skipped):
                delete = False
        if delete:
            path = dir / pathlib.Path(item)
            if os.path.isdir(path):
                delete_content(path, to_skip)
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
                delete_content(path, [])
                os.rmdir(path)
                print(f"[REMOVED]: {path}")
            else:
                clean_pycache(path)

def clean_config(to_skip : list[str]) -> None:
    config_path = pathlib.Path(f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\{PROJECT_OWNER}\\{PROJECT_NAME}")
    if os.path.exists(config_path):
        delete_content(config_path, to_skip)
        if not to_skip:
            print("[CONFIG]: Found config directory! Deleting...")
            os.rmdir(config_path)
    else:
        print("[CONFIG]: Did not find a config directory.")

def simple_argparse(args : list[str]) -> list[str]:
    skip = set()
    for arg in args:
        if arg.startswith("-"):
            for criteria in arg:
                match criteria:
                    case "c":
                        skip.add(".toml")
                    case _:
                        print(f"Unknown criteria: '{criteria}'")
    return list(skip)

if __name__ == "__main__":
    parsed_args = simple_argparse(sys.argv[1:])
    
    print("[PYCACHE]: Cleaning pycache...")
    clean_pycache(os.curdir)
    print("[PYCACHE]: Done cleaning pycache!")
    
    clean_config(parsed_args)

    # TODO Also clear database if it exists.