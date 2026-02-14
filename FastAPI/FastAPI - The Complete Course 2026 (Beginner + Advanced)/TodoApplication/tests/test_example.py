def test_instance():
    assert isinstance(1, int)
    assert isinstance("Hello", str)
    assert isinstance([1, 2, 3], list)


def test_equality():
    assert 1 + 1 == 2
    assert "Hello".upper() == "HELLO"
    assert len([1, 2, 3]) == 3


def test_boolean():
    assert True
    assert True != False
    assert ("Hello" == "World") is False


def test_list():
    num_list = [1, 2, 3]
    any_list = [False, True]

    assert 1 in num_list
    assert 5 not in num_list
    assert False in any_list
    assert all(num_list)
    assert any(any_list)


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


import pytest

@pytest.fixture
def default_person():
    return Person("albert", 25)

def test_person(default_person):
    person1 = default_person
    assert person1.name == "albert", "Expected name to be 'albert'"
    assert person1.age == 25, "Expected age to be 25"
