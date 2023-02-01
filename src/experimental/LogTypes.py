import datetime
import enum

class LogLevel(enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DATA = "DATA"
    DEBUG = "DEBUG"

class LogMessage:
    
    source : str
    level : LogLevel
    creation : datetime.datetime
    
    def __init__(self, source : str, level : LogLevel) -> None:
        self.creation = datetime.datetime.now()
        self.source = source.upper()
        self.level = level

class LoggerMessage(LogMessage):
    
    def __init__(self) -> None:
        super().__init__("logger")

class ObservationPhaseMessage(LogMessage):
    
    def __init__(self) -> None:
        super().__init__("simulation")
    
    def add_data(self, data) -> None:
        ...