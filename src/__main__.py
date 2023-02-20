import Simulation
from Common import Species
import Config

import LoggingHandler
from LoggingHandler.LogTypes import Message, LogLevel

if __name__ == "__main__":
    config = Config.ProjectConfigHandler()
    logger = LoggingHandler.Logger()
    print(f"Logger status is: {logger.is_running()}")
    logger.change_output_dir(config.config_root)

    brd = Simulation.create_new_board((5, 4), {
        #Species.BaseSpecie(0, "bear", [1], True, True): 50,
        Species.BaseSpecie(1, "deer", [2], True, True): 1,
        Species.BaseSpecie(2, "plant", [3], False, False): 50,
    })

    sim = Simulation.Simulation(brd, 0.1)

    for idx in range(100):
        print(f"Step {idx}")
        
        logger.new_message(Message(
            "simulation", LogLevel.DATA, sim.export_dict(),
        ))
        
        sim.step()
        

    logger.new_message(Message(
        "simulation", LogLevel.DATA, sim.export_dict(),
    ))

    logger.stop()