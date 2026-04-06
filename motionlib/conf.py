import json


class Conf(dict):
    def __init__(self, conf_path):
        with open(conf_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        super().__init__(data)
        self.__dict__ = self
