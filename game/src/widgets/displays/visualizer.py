


class Visualizer:
    def __init__(self, style, parent, context):
        self.style = style
        self.parent = parent
        self.context = context
        self.buffer = self.context.net.data_buffer
