
import logging

class Signal:
    def __init__(self) -> None:
        self.listeners = []

    def attach(self, listener, method):
        if not callable(getattr(listener, method)):
            logging.warning(f"Could not attach signal {self} to listener {listener}. Listener's method {method} is not callable")
            return
        self.listeners.append((listener, method))
    
    def detach(self,listener):
        listener_index = 0
        while listener_index <= len(self.listeners) - 1:
            if self.listeners[listener_index][0] is listener:
                self.listeners.pop(listener_index)
                return
            else:
                listener_index += 1

    def emit(self, *args):
        if self.listeners == []:
            return
        
        listener_index = 0
        while listener_index <= len(self.listeners) - 1:
            if self.listeners == []:
                return
            try:
                getattr(self.listeners[listener_index][0], self.listeners[listener_index][1])(*args)          
            except NotImplementedError:
                logging.warning(f"no entity exists for this signal")
                self.listeners.pop(listener_index)
            else:
                listener_index += 1
            

