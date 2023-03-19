import toml
import pathlib

DEFAULT_CONFIG = {
    "logger": {
        "db": {
            "uri": "mongodb://admin:admin@localhost",
            "port": 3001,
            "username": "admin",
            "password": "admin",
            "collection_name": "simdata",
        }
    },
    "simulation": {
        "width": 5.0,
        "height": 4.0,
        "grid_size": 3.0,
        "time_delta": 0.01,
        "num_steps": 10,
        "static_entity_spawn_rate": 5,
        "static_entity_spawn_interval": 3,
        "static_entity_max": 500,
    },
    "evolution": {
        "mutability": 0.1,
        "max_children": 8,
    },
    "entities": {
        "hunger_speed_multiplier": 0.1,
        "short_term_memory_span": 3.0,
        "long_term_memory_span": 5.0,
        "prey_saturation": 0.3,
    },
    "species": {
        "bear": {
            "id": 0,
            "prey": [1],
            "can_move": True,
            "can_see": True,
            "start_amount": 2,
        },
        "deer": {
            "id": 1,
            "prey": [2],
            "can_move": True,
            "can_see": True,
            "start_amount": 10,
        },
        "plant": {
            "id": 2,
            "prey": [],
            "can_move": True,
            "can_see": True,
            "start_amount": 50,
        },
    },
}

def genDefaultConfig(path : str | pathlib.Path) -> None:
    with open(path, "w+") as file:
        toml.dump(DEFAULT_CONFIG, file)
        print(f"Wrote default configuration to '{path}'.")