from utils.inputs.controls import Inputs


class Menu:
    def __init__(self, name):
        self.name = name
        self.inputs_queue = Inputs()
        self.elems = []

    def activity(self, **kwargs):
        pass

    def draw(self, surface):
        pass

    def add_queue(self, element):
        if element not in self.inputs_queue:
            self.inputs_queue.add(element)

    def add_raw_queue(self, element):
        if element not in self.inputs_queue.raw_inputs:
            self.inputs_queue.raw_add(element)

    def get_queue(self):
        temp = self.inputs_queue.copy()
        self.inputs_queue = Inputs()
        return temp
