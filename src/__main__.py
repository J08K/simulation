import LoggingHandler
import Config
import scoring

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
    
    print(scoring.max_delta_distance([
        (-9.0, 7.0),
        (-5.0, 5.0),
        (-10.0, 2.0),
        (-4.0, 0.0)
    ]))