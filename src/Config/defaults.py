from Config import data as ConfigData

DEFAULT_SIMULATION_CONFIG = ConfigData.SimulationConfig(
    max_agents=1000,
    start_agents=100,
    time_delta=0.1,
    num_steps=100_000,
)

DEFAULT_CONFIG = ConfigData.Config(
    sim_conf=DEFAULT_SIMULATION_CONFIG
)