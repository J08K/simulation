import os
import pathlib

IGNORE_DIRS = [".git", ".vscode"]
SHOULD_CONTAIN = ["__version__"]

def find_init_files(dir : pathlib.Path) -> pathlib.Path:
    dir_items = os.listdir(dir)
    if "__init__.py" in dir_items:
        yield dir / "__init__.py"
    
    for item in dir_items:
        path = dir / item
        if os.path.isdir(path) and not item in IGNORE_DIRS:
            for init_file in find_init_files(path):
                yield init_file

def contains_requirements(file_path : pathlib.Path) -> set[str]:
    not_found = [req for req in SHOULD_CONTAIN]
    with open(file_path, "r") as file:
        for line in file.readlines():
            for requirement in SHOULD_CONTAIN:
                if requirement in line.strip() and requirement in not_found:
                    not_found.remove(requirement)
    return not_found

if __name__ == "__main__":
    faults = 0
    files_found = 0
    for init_file in find_init_files(pathlib.Path(os.curdir)):
        files_found += 1
        result = contains_requirements(init_file)
        if result:
            faults += len(result)
            print(f"File: {init_file} does not contain: ")
            for requirement in result:
                print(f" - '{requirement}'")

    total_criteria = files_found * len(SHOULD_CONTAIN)

    print()
    print(f"Amount of faults: {faults}")
    print(f"Integrity: {round(((total_criteria - faults) / total_criteria) * 100, 2)}%")