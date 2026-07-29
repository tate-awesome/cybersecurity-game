


class AnimationManager:
    '''
    Global manager for animation loops. A single interruptor is more performant than an interruptor for every canvas.
    '''
    def __init__(self, root, frame_time_ms = 100):
        self.root = root
        self.callbacks = {}  # Stores identifier: callback_function
        self.run = True
        self.time = frame_time_ms

        self.start_loop()

    def add_callback(self, name: str, callback_func):
        """
        Dynamically an animation callback function
        """
        if name in self.callbacks.keys():
            print(f"[AnimationManager] Replaced callback: '{name}'")
        else:
            print(f"[AnimationManager] Added callback: '{name}'")
        self.callbacks[name] = callback_func

    def remove_callback(self, name: str):
        """
        Dynamically remove an animation callback function by its name.
        """
        if name in self.callbacks:
            del self.callbacks[name]
            print(f"[AnimationManager] Removed callback: '{name}'")

    def start_loop(self):
        self.run = True
        self.do_loop()
        
    def do_loop(self, event=None):
        """
        The single source of truth. Loops through and safely runs all registered 
        functions in a single pass.
        """
        # Iterate over a copy of the values to prevent runtime errors 
        # if a callback removes a callback mid-execution.
        active_callbacks = list(self.callbacks.values())
        
        for callback in active_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"[AnimationManager] Error executing callback: {e}")
        if self.run:
            self.root.after(self.time, self.do_loop)

    def stop_loop(self):
        self.run = False