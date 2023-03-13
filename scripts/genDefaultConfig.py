import toml

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
    },
    "evolution": {
        "mutability": 0.1
    },
    "entities": {
        "hunger_speed_multiplier": 0.1,
        "short_term_memory_span": 3.0,
        "long_term_memory_span": 5.0,
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
            "can_move": False,
            "can_see": False,
            "start_amount": 50,
        },
    },
}

if __name__ == "__main__":

    path = "default_config.toml"

    with open(path, "w+") as file:
        toml.dump(DEFAULT_CONFIG)
        print(f"Wrote default configuration to '{path}'.")
