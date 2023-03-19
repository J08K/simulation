import Simulation
import Config

import LoggingHandler
from LoggingHandler.LogTypes import Message, LogLevel
from rich.progress import track
import time

BREATHER_INTERVAL = 5

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
                old = logger.approx_size()
                print("1000 (more) steps have been taken!")
                print("Taking a breather!")
                while True:
                    if logger.approx_size() <= 0:
                        break
                    print(f"Not empty yet, taking a {BREATHER_INTERVAL} second sleep!")
                    time.sleep(BREATHER_INTERVAL)
                print(f"Went from {old} to {logger.approx_size()} items in queue.")
                print(f"Queue in-memory size is now: {logger.memory_size()}")
            

        logger.new_message(Message(
            "simulation", LogLevel.DATA, sim.export_dict(),
        ))
