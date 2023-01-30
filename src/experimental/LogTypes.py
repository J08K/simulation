import datetime
from ..board import ... # TODO WHAT SHOULD I DO?

class Log:
    
    creation : datetime.datetime
    
    def __init__(self) -> None:
        self.creation = datetime.datetime.now()
    


class ObservationPhaseLog(Log):
    
    def __init__(self) -> None:
        super().__init__()
    
    def add_data(self, data) -> None:
        