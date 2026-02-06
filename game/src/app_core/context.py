'''
Shared data for a game session. Passed to next pages on navigation
'''

class Context:

    def __init__(self, root, router):
        self.net = None
        self.progress = None
        self.router = router
        self.root = root