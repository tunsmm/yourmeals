from typing import Callable
import datetime
import os
import json

import numpy as np


def dict_to_date(date_dict: dict) -> datetime.date:
    return datetime.date(
        year=date_dict['year'],
        month=date_dict['month'],
        day=date_dict['day'],
    )


def dict_to_time(time_dict: dict) -> datetime.time:
    return datetime.time(
        hour=time_dict['hour'],
        minute=time_dict['minute'],
    )


def json_default(obj):
    if isinstance(obj, datetime.date):
        return dict(
            year=obj.year, 
            month=obj.month, 
            day=obj.day, 
        )
    elif isinstance(obj, datetime.time):
        return dict(
            hour=obj.hour, 
            minute=obj.minute,
        )
    else:
        return obj.__dict__


def toJSON(self):
    return json.dumps(self, default=lambda o: json_default(o), indent=4)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def dishes_cache(func: Callable):
    def wrapper(*args):
        filename = f'yourmeals/cache/{func.__name__}.npy'
        if os.path.exists(filename):
            result = np.load(filename, allow_pickle=True)
        else:
            result = func(*args)
            np.save(filename, result)
        return result
    return wrapper
