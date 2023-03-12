import Simulation
from Common import Species
import Config

import LoggingHandler
from LoggingHandler.LogTypes import Message, LogLevel

if __name__ == "__main__":
    config = Config.ProjectConfigHandler()
    with LoggingHandler.Handler() as logger:
        print(f"Logger status is: {logger.is_running()}")
        logger.change_output_dir(config.config_root)

        brd = Simulation.create_new_board((config.config.Simulation.width, config.config.Simulation.height), {
            Species.BaseSpecie(val["id"], spec, val["prey"], val["can_move"], val["can_see"]):val["start_amount"] for spec, val in config.config.Species.species.items()
        })

        sim = Simulation.Simulation(brd, config.config)

        for idx in range(config.config.Simulation.num_steps):
            print(f"Step {idx}")
            
            logger.new_message(Message(
                "simulation", LogLevel.DATA, sim.export_dict(),
            ))
            
            sim.step()
            

        logger.new_message(Message(
            "simulation", LogLevel.DATA, sim.export_dict(),
        ))
