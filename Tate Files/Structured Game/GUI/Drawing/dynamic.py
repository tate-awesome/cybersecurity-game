from customtkinter import CTkCanvas




class map:
    '''
    Dynamic zoomable, pannable map with position reset
    '''
    def __init__(self, parent):
        '''
        Places the new canvas in the parent
        '''
        self.current_zoom = 1.0
        self.current_pan = [0.0, 0.0]
        self.canvas = CTkCanvas()
    
    