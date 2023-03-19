import Simulation
import Config

import LoggingHandler
from LoggingHandler.LogTypes import Message, LogLevel
from rich.progress import track

if __name__ == "__main__":
    config = Config.ProjectConfigHandler()
    with LoggingHandler.Handler(config.config.Logger) as logger:
        print(f"Logger status is: {logger.is_running()}")
        logger.change_output_dir(config.config_root)

        brd = Simulation.create_new_board(config.config)

        sim = Simulation.Simulation(brd, config.config)

        for idx in track(range(config.config.Simulation.num_steps), description="Simulating...", total=config.config.Simulation.num_steps):
            
            logger.new_message(Message(
                "simulation", LogLevel.DATA, sim.export_dict(),
            ))
            
            sim.step()

            if sim.reproduction_count != 0 and sim.reproduction_count % 1000 == 0:
                print("1000 (more) entities have been born!")
            
            if sim.steps_taken % 1000 == 0:
                print("1000 (more) steps have been taken!")
            

        logger.new_message(Message(
            "simulation", LogLevel.DATA, sim.export_dict(),
        ))
