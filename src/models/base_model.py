import json


class BaseModel:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
