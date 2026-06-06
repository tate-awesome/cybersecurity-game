


class Visualizer:
    def __init__(self, parent, context):
        self.style = context.style
        self.parent = parent
        self.context = context
        self.buffer = self.context.net.data_buffer
