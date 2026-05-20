import json
import os


class Storage:
    def __init__(self, filename="data.json"):
        self.filename = filename

        if not os.path.exists(self.filename):
            self.save_data({})

    def load_data(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
        except FileNotFoundError:
            return {}
        except Exception:
            return {}

    def save_data(self, data):
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as error:
            print(f"Storage error: {error}")