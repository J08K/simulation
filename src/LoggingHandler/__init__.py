import threading
import queue
import datetime
import pathlib
import os
import io

from LoggingHandler import LogTypes
from LoggingHandler.LogTypes import CommandType, LogLevel

__version__ = "0.0.1"

class Logger:
    
    writer_thread : threading.Thread
    run_thread : bool

    __queue : queue.Queue[LogTypes.Message | LogTypes.Command]
    __verbosity : int
    __output_file_path : pathlib.Path | None
    
    def __writer(self) -> None:
        
        self.__verbosity = 0
        self.__output_file_path = None

        file_obj : io.TextIOWrapper = None # TODO Make sure that this is checked, and or make it so that this is put in a temp folder.

        # * The only thing this function needs to do is to handle the outputting of WELL STRUCTURED inputs.
        # TODO Let this thread do more computing, to take the load of the main thread.
        
        def create_new_file(file_path : pathlib.Path) -> pathlib.Path:
            idx = 1
            extension = file_path.suffix
            new_file_path = str(file_path.absolute())[:-len(extension)] # Gets absolute path without file extension.
            
            if os.path.exists(new_file_path + extension):
                while os.path.exists(new_file_path + "_" + str(idx) + extension):
                    idx += 1
                new_file_path = new_file_path + "_" + str(idx) + extension
            return pathlib.Path(new_file_path)

        def open_new_path(dir_path : pathlib.Path) -> pathlib.Path:
            selected_path = None
            if "." in str(dir_path): # Check if path given is to a file.
                selected_path = create_new_file(dir_path)
            else:
                file_name = datetime.datetime.now().strftime("%Y_%m_%d") + ".log"
                selected_path = create_new_file(dir_path / file_name)
            
            file_obj = open(selected_path, "w+")

            return selected_path

        def handle_message(msg : LogTypes.Message) -> None:
            # TODO Handle messages properly, like store them.
            # TODO Add message exporting, like sending them to a database or server.
            print(f"[{datetime.datetime.now()}]: {msg}")
        
        def handle_command(cmd : LogTypes.Command) -> None:
            match cmd.command_type:
                case CommandType.FILE_CHANGE:
                    new_output_dir = open_new_path(pathlib.Path(cmd.command_type))
                    handle_message(LogTypes.Message(
                        source="logger",
                        level=LogLevel.INFO,
                        data=f"Changing log file location to '{str(new_output_dir)}'",
                    ))
                case CommandType.END_LOG:
                    self.run_thread = False
                    for message in self.__queue.queue:
                        handle_message(message)

                    handle_message(LogTypes.Message(
                        source="logger",
                        level=LogLevel.INFO,
                        data=f"End of log. {str(cmd.command_data)}",
                    ))
                    file_obj.close()

                case CommandType.CHANGE_VERBOSITY:
                    self.__verbosity = cmd.command_data
                    handle_message(LogTypes.Message(
                        source="logger",
                        level=LogLevel.INFO,
                        data=f"Verbosity is now {str(cmd.command_data)}.",
                    ))
                case CommandType.DUMMY:
                    handle_message(LogTypes.Message(
                        source="logger",
                        level=LogLevel.DEBUG,
                        data=f"Ran Dummy logger command. {str(cmd.command_data)}",
                    ))
                case _:
                    raise TypeError(f"Unknown command type: {str(cmd)}")

        while self.run_thread:
            message = self.__queue.get()
            if message:
                if isinstance(message, LogTypes.Command):
                    handle_command(message)
                elif isinstance(message, LogTypes.Message):
                    handle_message(message)

    def __init__(self) -> None:
        self.writer_thread = threading.Thread(target=self.__writer)
        self.__queue = queue.Queue()
        self.run_thread = True
        self.writer_thread.start()
    
    def new_message(self, message : str) -> None:
        if self.run_thread:
            self.__queue.put(message)
        else:
            ... # TODO Probably add some kind of exception when trying to add logs to a stopped logger?
        
    def stop(self) -> None:
        self.run_thread = False
        self.__queue.put(LogTypes.Command(
            LogTypes.CommandType.END_LOG,
            "ENDED LOG"
        ))