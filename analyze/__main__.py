from typing import Any
import pymongo
import pymongo.collection
import os
import sqlite3

URI = "localhost"
PORT = 3001
USERNAME = "admin"
PASSWORD = "admin"
DB_NAME = "simulationdb"
FULL_URI = f"mongodb://{USERNAME}:{PASSWORD}@{URI}:{PORT}"

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
    
    def get_species_counts(self) -> list[dict[str, Any]]:
        res = list(self.client.aggregate([
            {
                "$project": {
                    "_id": "$time_current",
                    "species": "$board.specie_stats",
                }
            }
        ]))
        return [{
            "time": doc["_id"],
            "species": [{"id": specie["specie"]["id"], "name": specie["specie"]["name"], "count": specie["count"]} for specie in doc["species"]],
            } for doc in res]

def construct_sim(num : int) -> Simulation:
    return Simulation(BASE_COLLECTION_NAME + " " + str(num))

if __name__ == "__main__":

    if not os.path.exists("./output"):
        os.mkdir("./output")

    sim = construct_sim(2)

    db_filepath = f"./output/{sim.sim_name}.db"

    if os.path.exists(db_filepath):
        print(f"Deleting '{db_filepath}'")
        os.remove(f"./output/{sim.sim_name}.db")

    conn = sqlite3.connect(db_filepath)
    cursor = conn.cursor()

    # //////////////////////////////////////////////////
    # Entity count
    
    cursor.execute("CREATE TABLE entity_count (time REAL PRIMARY KEY, entity_num INTEGER)")
    
    for item in sim.get_entity_counts():
        value = ','.join([str(idx) for idx in item.values()])
        cursor.execute(f"INSERT INTO entity_count VALUES ({value})")

    conn.commit()

    # //////////////////////////////////////////////////
    # Specie count
    
    cursor.execute("CREATE TABLE specie_count (time REAL, specie_id INTEGER, specie_name TEXT, count INTEGER)")

    for item in sim.get_species_counts():
        for specie in item["species"]:
            value = f'{item["time"]}, {specie["id"]}, "{specie["name"]}", {specie["count"]}'
            cursor.execute(f"INSERT INTO specie_count VALUES ({value})")

    conn.commit()
    
    # //////////////////////////////////////////////////
    
    cursor.close()
    conn.close()