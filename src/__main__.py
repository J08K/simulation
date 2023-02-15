import json
import Simulation
from Common import Species
import timeit

if __name__ == "__main__":
    """ config = Config.ProjectConfigHandler()
    logger = LoggingHandler.Logger()
    print(f"Logger status is: {logger.is_running()}")

    logger.new_message(LoggingHandler.LogTypes.Message(
        source="the outside",
        level=LoggingHandler.LogLevel.DEBUG,
        data="This should be in a temp directory."
    ))

    logger.change_output_dir(config.config_root)

    logger.new_message(LoggingHandler.LogTypes.Message(
        source="the outside again",
        level=LoggingHandler.LogLevel.DEBUG,
        data="This should be in a better, more suitable location!"
    ))

    logger.stop()

    print("Logger has stopped!") """

    brd = Simulation.create_new_board((16, 10), {
        Species.BaseSpecie(0, "bear", [1], True, True): 5,
        Species.BaseSpecie(1, "deer", [2], True, True): 20,
        Species.BaseSpecie(2, "plant", [3], False, False): 30,
    })

    entity = brd.all_entities[0]

    with open("entity.json", "w+") as file:
        json.dump(entity.export_dict(), file, indent=4)