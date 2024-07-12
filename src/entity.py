class Entity:
    def __init__(self) -> None:
        self._id = None
        self._name = None
    
    def set_name(self, name):
        self._name = name
    
    def get_name(self):
        name = self._name
        return name
    
    def set_id(self, id):
        self._id = id
    
    def get_id(self):
        id = self._id
        return id

    def update(self, delta):
        pass

    def draw(self):
        pass