from typing import Any
import pymongo
import pymongo.collection

from analyze import config

class Simulation:

    sim_name: str
    client: pymongo.collection.Collection[dict[str, Any]]

    def __init__(self, sim_name : str) -> None:
        self.sim_name = sim_name
        self.client = pymongo.MongoClient(config.FULL_URI)[config.DB_NAME][sim_name]

    def get_entity_counts(self) -> list[dict[str, Any]]:
        res = list(self.client.aggregate([{"$project": {"_id": "$time_current", "num_entities": {"$size": "$board.entities"}}}]))
        return res
