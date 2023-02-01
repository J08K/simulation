import LoggingHandler
import Config

if __name__ == "__main__":
    config = Config.ProjectConfigHandler()
    logger = LoggingHandler.Logger()
    print(f"Logger status is: {logger.is_running()}")

    logger.new_message(LoggingHandler.LogTypes.Message(
        source="the outside",
        level=LoggingHandler.LogLevel.DEBUG,
        data="This should be in a temp directory."
    ))

    logger.change_output_dir("C:\\Users\\jobko\\Test")

    logger.new_message(LoggingHandler.LogTypes.Message(
        source="the outside again",
        level=LoggingHandler.LogLevel.DEBUG,
        data="This should be in a better, more suitable location!"
    ))

    logger.stop()

    print("Logger has stopped!")