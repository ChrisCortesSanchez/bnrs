"""
This file deals with our city-level data.
"""
import data.db_connect as db_connect

MIN_ID_LEN = 1

CITY_COLLECTION = 'cities'

ID = 'id'
NAME = 'name'
STATE_CODE = 'state_code'

SAMPLE_CITY = {
    NAME: 'New York',
    STATE_CODE: 'NY',
}

city_cache = {}


def is_valid_id(_id: str) -> bool:
    if not isinstance(_id, str):
        return False
    if len(_id) < MIN_ID_LEN:
        return False
    return True


def num_cities() -> int:
    return len(read())


def create(flds: dict) -> str:
    print(f'{flds=}')
    if not isinstance(flds, dict):
        raise ValueError(f'Bad type for {type(flds)=}')
    if not flds.get(NAME):
        raise ValueError(f'Bad value for {flds.get(NAME)=}')
    new_id = db_connect.create(CITY_COLLECTION, flds)
    print(f'{new_id=}')
    return new_id


def delete(name: str, state_code: str) -> bool:
    filter_query = {
        NAME: name,
        STATE_CODE: state_code,
    }
    ret = db_connect.delete(CITY_COLLECTION, filter_query)
    if ret < 1:
        raise ValueError(f'City not found: {name}, {state_code}')
    return ret


def read() -> list:
    return db_connect.read(CITY_COLLECTION)


def main():
    print(read())


if __name__ == '__main__':
    main()
