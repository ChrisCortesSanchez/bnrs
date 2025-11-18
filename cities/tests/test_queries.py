import pytest
from copy import deepcopy
from unittest.mock import patch
import cities.queries as qry


def get_temp_rec():
    return deepcopy(qry.SAMPLE_CITY)

@pytest.fixture(scope='function')
def temp_city_no_del():
    temp_rec = get_temp_rec()
    qry.create(get_temp_rec())
    return temp_rec


@pytest.mark.skip('This is an example of a bad test!')
def test_bad_test_for_num_cities():
    assert qry.num_cities() == len(qry.city_cache)

@pytest.fixture(scope='function')
def temp_city():
    temp_rec = get_temp_rec()
    new_rec_id = qry.create(get_temp_rec())
    yield new_rec_id
    try:
        qry.delete(temp_rec[qry.NAME], temp_rec[qry.STATE_CODE])
    except ValueError:
        print('The record was already deleted.')


def test_num_cities():
    # get the count
    old_count = qry.num_cities()
    # add a record
    qry.create(qry.SAMPLE_CITY)
    assert qry.num_cities() == old_count + 1


def test_good_create():
    old_count = qry.num_cities()
    qry.create(get_temp_rec())
    assert qry.num_cities() == old_count + 1


def test_create_bad_name():
    with pytest.raises(ValueError):
        qry.create({})


def test_create_bad_param_type():
    with pytest.raises(ValueError):
      qry.create(17)

def test_read(temp_city):
    cities = qry.read()
    assert isinstance(cities, list)
    assert get_temp_rec() in cities


@patch('cities.queries.db_connect', return_value=False, autospec=True)
def test_read_cant_connect(mock_db_connect):
    with pytest.raises(ConnectionError):
        cities = qry.read()


@pytest.fixture(scope='function')
def test_city():
    new_rec_id = qry.create(qry.SAMPLE_CITY)
    yield new_rec_id


def test_delete(temp_city_no_del):
    ret = qry.delete(temp_city_no_del[qry.NAME], temp_city_no_del[qry.STATE_CODE])
    assert ret == 1


@patch('cities.queries.db_connect', return_value=True, autospec=True)
def test_delete_not_there(mock_db_connect):
    with pytest.raises(ValueError):
        qry.delete('some city name that is not there', 'not a state')


# Additional fixture for creating multiple cities
@pytest.fixture(scope='function')
def multiple_cities():
    """Fixture that creates multiple test cities and cleans up"""
    city_ids = []
    for i in range(3):
        city_id = qry.create({
            qry.NAME: f'TestCity{i}',
            qry.STATE_CODE: f'T{i}'
        })
        city_ids.append(city_id)
    yield city_ids
    # Cleanup
    for city_id in city_ids:
        if city_id in qry.city_cache:
            qry.delete(city_id)


# Additional raises to test for deleting a citiy twice
def test_delete_twice_raises_error(test_city):
    """Test that deleting same city twice raises ValueError"""
    qry.delete(test_city)
    with pytest.raises(ValueError, match='No such city'):
        qry.delete(test_city)
