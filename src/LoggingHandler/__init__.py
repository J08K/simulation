import threading
import queue
import datetime
import pathlib
import os
import io
import tempfile
import pymongo
import sys

from typing import Any
from rich.progress import track

from Common import cycle_names

from Config import ConfigData

from LoggingHandler import LogTypes
from LoggingHandler.LogTypes import CommandType, LogLevel

__version__ = "0.0.2"

class Logger:
    
    writer_thread : threading.Thread
    
    config : ConfigData.LoggerConfig

    __run_thread : bool
    __queue : queue.Queue[LogTypes.Message | LogTypes.Command]
    __verbosity : int
    __output_file_path : pathlib.Path | None
    __is_temp_dir : bool
    __file_obj : io.TextIOWrapper
    __mongo_collection : pymongo.collection.Collection
    
    def __writer(self) -> None:

        self.__verbosity = 0

        self.__output_file_path = None
        self.__is_temp_dir = True
        self.__file_obj : io.TextIOWrapper = tempfile.TemporaryFile()

        def getCollection(database : pymongo.database.Database) -> Any | None:
            coll_names = database.list_collection_names()
            for collection_name in cycle_names(self.config.db_collection_name, " ", False, 1):
                if collection_name not in coll_names:
                    return database[collection_name]

        def create_new_file(file_path : pathlib.Path) -> pathlib.Path:
            idx = 1
            extension = file_path.suffix
            new_file_path = str(file_path.absolute())[:-len(extension)] # Gets absolute path without file extension.
            if os.path.exists(new_file_path + extension):
                while os.path.exists(new_file_path + "_" + str(idx) + extension):
                    idx += 1
                new_file_path = new_file_path + "_" + str(idx)
            return pathlib.Path(new_file_path + extension)

        def open_new_path(dir_path : pathlib.Path) -> pathlib.Path:
            selected_path = None
            if "." in str(dir_path): # Check if path given is to a file.
                selected_path = create_new_file(dir_path)
            else:
                file_name = datetime.datetime.now().strftime("%Y_%m_%d") + ".log"
                selected_path = create_new_file(dir_path / file_name)
            
            self.__output_file_path = selected_path
            if self.__is_temp_dir:
                temp_file = self.__file_obj
                self.__file_obj = open(selected_path, "w+b")
                temp_file.seek(0) # TODO Find out WTF seek is! (01-Feb-2023)
                for line in temp_file.readlines():
                    self.__file_obj.write(line)
                temp_file.close()
                self.__is_temp_dir = False
            else:
                self.__file_obj.close()
                self.__file_obj = open(selected_path, "w+b")

            return selected_path

        def handle_message(msg : LogTypes.Message) -> None:
            # TODO Add message exporting, like sending them to a database or server.
            if msg.level == LogLevel.DATA:
                data_id = self.__mongo_collection.insert_one(msg.get_data())
                self.new_message(LogTypes.Message(
                    "logger", LogLevel.INFO, f"Inserted data into collection with id: '{str(data_id)}'."
                ))
            elif msg.level.value >= self.__verbosity:
                self.__file_obj.write(bytes(f"\n[{str(msg.creation)}][{msg.level.name}][{msg.source}]:{msg.get_data()}", encoding="UTF-8"))
        
        def handle_command(cmd : LogTypes.Command) -> None:
            match cmd.command_type:
                case CommandType.FILE_CHANGE:
                    new_output_dir = open_new_path(pathlib.Path(cmd.command_data))
                    handle_message(LogTypes.Message(
                        source="logger",
                        level=LogLevel.INFO,
                        data=f"Changing log file location to '{str(new_output_dir)}'",
                    ))
                case CommandType.END_LOG:
                    self.__run_thread = False

                    # * By now, should not have any messages to process anyway.

                    handle_message(LogTypes.Message(
                        source="logger",
                        level=LogLevel.INFO,
                        data=f"End of log. {str(cmd.command_data)}",
                    ))
                    self.__file_obj.close()

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

        db_url = f"mongodb://{self.config.db_username}:{self.config.db_password}@{self.config.db_uri}:{str(self.config.db_port)}"
        mongo_client = pymongo.MongoClient(db_url)
        self.new_message(LogTypes.Message(
            "logger", LogLevel.INFO, f"Client connected on url: {db_url}",
        ))
        database = mongo_client["simulationdb"]
        self.new_message(LogTypes.Message(
            "logger", LogLevel.INFO, "Database connected!",
        ))
        self.__mongo_collection = getCollection(database)
        self.new_message(LogTypes.Message(
            "logger", LogLevel.INFO, f"Created new collection '{self.__mongo_collection.name}'",
        ))

        while self.__run_thread:
            message = self.__queue.get()
            if message:
                if isinstance(message, LogTypes.Command):
                    handle_command(message)
                elif isinstance(message, LogTypes.Message):
                    handle_message(message)

        remaining = list(self.__queue.queue)
        for item in track(remaining, description="Handling remaining messages...", total=len(remaining)):
            if item:
                if isinstance(item, LogTypes.Command):
                    handle_command(item)
                elif isinstance(item, LogTypes.Message):
                    handle_message(item)
        

    def __init__(self, config : ConfigData.LoggerConfig) -> None:
        self.config = config

        self.writer_thread = threading.Thread(target=self.__writer)
        self.__queue = queue.Queue()
        self.__run_thread = True

        self.writer_thread.start()
    
    def new_message(self, message : LogTypes.Message) -> None:
        if self.__run_thread:
            self.__queue.put(message)
        # else:
        #     raise ValueError("Tried creating logger message, but logger has stopped!")

    def new_command(self, cmd : LogTypes.Command) -> None:
        if self.__run_thread:
            self.__queue.put(cmd)
        else:
            raise ValueError("Tried creating logger command, but logger has stopped!")

    def change_output_dir(self, new_path : str | pathlib.Path) -> None:
        new_path = pathlib.Path(new_path)
        self.new_command(LogTypes.Command(
            CommandType.FILE_CHANGE,
            str(new_path.absolute())
        ))

    def stop(self) -> None:
        self.__run_thread = False
        self.__queue.put(LogTypes.Command(
            LogTypes.CommandType.END_LOG,
            "ENDED LOG"
        ))
    
    def is_running(self) -> bool:
        return self.__run_thread
    
    def approx_size(self) -> int:
        return self.__queue.qsize()
    
    def memory_size(self) -> int:
        return sys.getsizeof(self.__queue)

class Handler:

    current_logger : Logger | None
    config: ConfigData.LoggerConfig

    def __init__(self, config : ConfigData.LoggerConfig) -> None:
        self.current_logger = None
        self.config = config
    
    def __enter__(self) -> Logger:
        if self.current_logger:
            raise ValueError("Tried creating a logger, when one has already been instantiated!")
        
        self.current_logger = Logger(self.config)
        return self.current_logger
    
    def __exit__(self, *args, **kwargs) -> None:
        self.current_logger.stop()
