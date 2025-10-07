# File for city level data

from random import randint

MIN_ID_LEN = 1

ID = "id"
NAME = 'name'
STATE_CODE = 'state_code'

city_cache = {}

SAMPLE_CITY = {NAME:'New York', STATE_CODE:'NY'}

def is_valid_id(id:str) -> bool:
    if not(isinstance(id, str)):
        return False
    if len(id) < MIN_ID_LEN:
        return False
    return True

def num_cities()->int:
    return len(city_cache)


def create(fields:dict)->str:
    if not(isinstance(fields, dict)):
        raise ValueError(f"Invalid type for {type(fields)=}")
    if not fields.get(NAME):
        raise ValueError(f"Invalid value for {fields.get(NAME)=}")
    
    new_id = str(len(city_cache) + 1)
    city_cache[new_id] = fields
    return new_id
