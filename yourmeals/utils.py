import json

import numpy as np
from os.path import exists
from typing import Callable


def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def numpy_cache(func: Callable):
    def wrapper(*args):
        filename = f'yourmeals/cache/{func.__name__}.npy'
        if exists(filename):
            result = np.load(filename, allow_pickle=True)
        else:
            result = func(*args)
            np.save(filename, result)
        return result

    return wrapper
