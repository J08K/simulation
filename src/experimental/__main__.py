import threading
import queue
import datetime

class Logger:
    
    writer_thread : threading.Thread
    run_thread : bool
    __messages : queue.Queue
    
    def __writer(self) -> None:
        
        def handle_message(msg) -> None:
            print(f"[{datetime.datetime.now()}]: {msg}")
        
        while self.run_thread:
            message = self.__messages.get()
            if message:
                handle_message(message)
            
        for message in self.__messages.queue:
            handle_message(message)
        
    
    def __init__(self) -> None:
        self.writer_thread = threading.Thread(target=self.__writer)
        self.__messages = queue.Queue()
        self.run_thread = True
        self.writer_thread.start()
    
    def new_message(self, message : str) -> None:
        if self.run_thread:
            self.__messages.put(message)
        else:
            ... # TODO Probably add some kind of exception when trying to add logs to a stopped logger?
        
    def stop(self) -> None:
        self.run_thread = False
        self.__messages.put("END")
        
log = Logger()
log.new_message("Start")
for idx in range(20):
    log.new_message(str(idx))
log.stop()
print("I am already here!")