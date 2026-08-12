import json, os

class Preferences:
    def __init__(self):
        '''
        Manages persistent data across multiple sessions.
        Created before the root in App().
        Other classes use it to populate their fields.
        '''
        self.data = dict()
        self.load()

    def load(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "..", "..", "assets", "preferences", "preferences.json")
        try:
            with open(file_path) as json_file:
                data = json.load(json_file)
        except:
            data = {}
            pass
        
        for key, value in data.items():
            self.data[key] = value

    def save(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "..", "..", "assets", "preferences", "preferences.json")
        with open(file_path, "w") as file:
            json.dump(self.data, file)

    def has(self, key: str):
        if key in self.data.keys() and len(self.data[key]) > 0:
            # print(f"{key}: {self.data[key]}")
            return True

    def get(self, key: str):
        return self.data.get(key)

    def set(self, key: str, value):
        self.data[key] = value
        self.save()

    def clear(self):
        self.data.clear()
        self.data = {
            "mode": "",
            "theme": "",
            "labels": {},
            "page": "",
            "panes": {}, # TODO save and load pane sizes between refreshes at least

            "settings": {}
        }
        self.save()