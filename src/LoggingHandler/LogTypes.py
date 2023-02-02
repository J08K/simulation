import datetime
import enum

from typing import Callable, Any

class CommandType(enum.Enum):
    FILE_CHANGE = 0         # * - Changes to the output file / directory. Data is new path.
    END_LOG = 1             # * - Telling the logger thread to stop. Data is optional message.
    CHANGE_VERBOSITY = 2   # * - Changing the what is output to the console. Data is new verbosity level. (Higher means less output)
    DUMMY = 3               # * - Just an empty command, run it to clean some cache? Data is optional message.

class Command():
    
    command_type : CommandType
    command_data : str | None

    def __init__(self, command_type : CommandType, command_data : str = None) -> None:
        self.command_type = command_type
        self.command_data = command_data


class LogLevel(enum.Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    DATA = 4


class Message:
    
    source : str
    level : LogLevel
    creation : datetime.datetime
    __data : str
    __parser : Callable[[Any], str]
    
    def __init__(self, source : str, level : LogLevel, data : str, parser : Callable[[Any], str] = str) -> None:
        self.creation = datetime.datetime.now()
        self.source = source.upper()
        self.level = level
        self.__data = data
        self.__parser = parser

    def get_data(self) -> str:
        return self.__parser(self.__data)

# TODO for data, add a function to parse it into a string. This makes it so that the computing is done on the Logging thread.
class ObservationPhaseMessage(Message):
    
    def __init__(self) -> None:
        super().__init__("simulation")
    
    def add_data(self, data) -> None:
        ...