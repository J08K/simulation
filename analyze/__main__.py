from typing import Any
import pymongo
import pymongo.collection
import csv
import os

URI = "localhost"
PORT = 3001
USERNAME = "admin"
PASSWORD = "admin"
DB_NAME = "simulationdb"
FULL_URI = db_url = f"mongodb://{USERNAME}:{PASSWORD}@{URI}:{PORT}"

BASE_COLLECTION_NAME = "simdata"

class Simulation:

    sim_name: str
    client: pymongo.collection.Collection[dict[str, Any]]

    def __init__(self, sim_name : str) -> None:
        self.sim_name = sim_name
        self.client = pymongo.MongoClient(FULL_URI)[DB_NAME][sim_name]

    def get_entity_counts(self) -> list[dict[str, Any]]:
        res = list(self.client.aggregate([
            {"$project": {
            "_id": "$time_current",
            "num_entities": {
                "$size": "$board.entities"
                }
            }},
        ]))
        return res

if __name__ == "__main__": 

    if not os.path.exists("./output"):
        os.mkdir("./output")

    sim = Simulation(BASE_COLLECTION_NAME + " 40")

    with open("./output/entity_count.csv", "w+", newline="") as file:
        writer = csv.DictWriter(file, ["time", "entity_num"], delimiter=";")
        writer.writeheader()
        for item in sim.get_entity_counts():
            writer.writerow({"time": item["_id"], "entity_num": item["num_entities"]})