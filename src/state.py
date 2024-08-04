import logging

class State:
    def __init__(self, states: dict, *args) -> None:
        self.name = None
        self.states: dict = states
        self.next_state: str = None
        self.previous_state: str = None
    
    def start(self,object,initial_state="init"):


        self.set_state(object,initial_state)
           
    def set_state(self, object, new_state, *args):
        if new_state in self.states:
            object.state.on_state_exit(object)

            if isinstance(self.states[new_state], tuple):
                next_state = self.states[new_state][0](self.states, *args)
            else:
                next_state = self.states[new_state](self.states, *args)
            next_state.previous_state = object.state.name
            object.state = next_state
            object.state.name = new_state
            object.state.on_state_enter(object)
        else:
            logging.debug(f'object {object.__class__.__name__} does not have a {new_state} state')
    
    def get_name(self):
        return self.name

    def on_state_enter(self,object):
        pass

    def on_state_exit(self,object):
        pass

    def process_events(self,object):
        pass

    def update(self,object):
        pass

    def draw(self,object):
        pass
    
    def set_previous_state(self, previous_state_name: str):
        if previous_state_name in self.states:
            self.previous_state = previous_state_name

    def set_next_state(self, next_state_name: str):
        if next_state_name in self.states:
            self.next_state = next_state_name