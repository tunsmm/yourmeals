from typing import Callable
import datetime
import json
import pickle
import os

import numpy as np


def convert_dicts_to_date_time(date_dict: dict, time_dict: dict) -> tuple[datetime.date, datetime.date]:
    return (
        dict_to_date(date_dict=date_dict), 
        dict_to_time(time_dict=time_dict)
    )


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


def toJSON(self) -> str:
    return json.dumps(self, default=lambda o: json_default(o), indent=4)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def numpy_cache(func: Callable):
    """Decorator to create some cache via npy format
    """
    def wrapper(*args):
        filename = f'yourmeals/cache/{func.__name__}.npy'
        if os.path.exists(filename):
            result = np.load(filename, allow_pickle=True)
        else:
            result = func(*args)
            np.save(filename, result)
        return result
    return wrapper


def cache(func: Callable):
    """Decorator to create some cache via pickle
    """
    def wrapper(*args):
        filename = f'yourmeals/cache/{func.__name__}.pickle'
        if os.path.exists(filename):
            with open(filename, 'rb') as fp:
                result = pickle.load(fp)
        else:
            result = func(*args)
            with open(filename, 'wb') as fp:
                pickle.dump(result, fp)
        return result
    return wrapper
