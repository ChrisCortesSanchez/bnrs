from copy import deepcopy
from unittest.mock import patch, MagicMock
import pytest

import cities.queries as qry


def get_temp_rec():
    return deepcopy(qry.SAMPLE_CITY)


# -----------------------------
# Fixtures
# -----------------------------

@pytest.fixture(scope='function')
def temp_city_no_del():
    temp_rec = get_temp_rec()
    with patch('cities.queries.db_connect.create', return_value="1234"):
        qry.create(get_temp_rec())
    return temp_rec


@pytest.fixture(scope='function')
def temp_city():
    temp_rec = get_temp_rec()
    with patch('cities.queries.db_connect.create', return_value="1234"):
        new_rec_id = qry.create(get_temp_rec())

    yield new_rec_id

    try:
        with patch('cities.queries.db_connect.delete', return_value=1):
            qry.delete(temp_rec[qry.NAME], temp_rec[qry.STATE_CODE])
    except ValueError:
        pass


# -----------------------------
# Professor’s Tests
# -----------------------------

@pytest.mark.skip('This is an example of a bad test!')
def test_bad_test_for_num_cities():
    assert qry.num_cities() == len(qry.city_cache)


def test_num_cities():
    with patch('cities.queries.db_connect.read', return_value=[]):
        old_count = qry.num_cities()

    with patch('cities.queries.db_connect.create', return_value="1234"):
        qry.create(get_temp_rec())

    with patch('cities.queries.db_connect.read', return_value=[get_temp_rec()]):
        assert qry.num_cities() == old_count + 1


def test_good_create():
    with patch('cities.queries.db_connect.read', return_value=[]):
        old_count = qry.num_cities()

    with patch('cities.queries.db_connect.create', return_value="1234"):
        new_rec_id = qry.create(get_temp_rec())
        assert qry.is_valid_id(new_rec_id)

    with patch('cities.queries.db_connect.read', return_value=[get_temp_rec()]):
        assert qry.num_cities() == old_count + 1


def test_create_bad_name():
    with pytest.raises(ValueError):
        qry.create({})


def test_create_bad_param_type():
    with pytest.raises(ValueError):
        qry.create(17)


def test_delete(temp_city_no_del):
    with patch('cities.queries.db_connect.delete', return_value=1):
        ret = qry.delete(temp_city_no_del[qry.NAME], temp_city_no_del[qry.STATE_CODE])
        assert ret == 1


def test_delete_not_there():
    with patch('cities.queries.db_connect.delete', return_value=0):
        with pytest.raises(ValueError):
            qry.delete('some city name that is not there', 'not a state')


def test_read(temp_city):
    mock_data = [get_temp_rec()]
    with patch('cities.queries.db_connect.read', return_value=mock_data):
        cities = qry.read()
        assert isinstance(cities, list)
        assert get_temp_rec() in cities


# -----------------------------
# Your additional (fixed) tests
# -----------------------------

@pytest.fixture(scope='function')
def multiple_cities():
    city_ids = []
    with patch('cities.queries.db_connect.create', side_effect=lambda *args: "id"):
        for i in range(3):
            city_id = qry.create({
                qry.NAME: f'TestCity{i}',
                qry.STATE_CODE: f'T{i}'
            })
            city_ids.append(city_id)
    return city_ids


def test_delete_twice_raises_error():
    # First delete succeeds
    with patch('cities.queries.db_connect.delete', return_value=1):
        qry.delete('New York', 'NY')

    # Second delete fails
    with patch('cities.queries.db_connect.delete', return_value=0):
        with pytest.raises(ValueError):
            qry.delete('New York', 'NY')
