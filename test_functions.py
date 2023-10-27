import pytest
from utils import sumvalues, maxvalue, minvalue, meannvalue, countvalue

def test_sumvalues():
    assert sumvalues([1, 2, 3]) == 6
    assert sumvalues(['4', '5', '6']) == 15
    assert sumvalues([]) == 0
    with pytest.raises(TypeError):
        sumvalues([[1, 2, 3], [4, 5, 6]])
        sumvalues(10)
        sumvalues('help')

def test_maxvalue():
    assert maxvalue([1, 2, 3]) == 2
    assert maxvalue(['4', '6', '5']) == 1
    with pytest.raises(TypeError):
        maxvalue([[1, 2, 3], [4, 5, 6]])
        maxvalue(10)
        maxvalue('hello')
        maxvalue([])

def test_minvalue():
    assert minvalue([1, 2, 3]) == 0
    assert minvalue(['5', '6', '4']) == 2
    with pytest.raises(TypeError):
        minvalue([[1, 2, 3], [4, 5, 6]])
        minvalue(10)
        minvalue('hello')
        minvalue([])

def test_meanvalue():
    assert meannvalue([1, 2, 3]) == 2
    assert meannvalue(['4', '5', '6']) == 5
    with pytest.raises(TypeError):
        meannvalue([[1, 2, 3], [4, 5, 6]])
        meannvalue(10)
        meannvalue('hello')
        meannvalue([])

def test_countvalue():
    assert countvalue([1, 1, 1, 2], 1) == 3
    assert countvalue([[1, 2, 3], [1, 1, 1]], 1) == 0