import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from flask import Flask
from use_cases.get_people import GetPeopleUseCase
from repositories.people_repository import PeopleRepository
from main import app as flask_app
from entities.person import Person
import json


# Fixtures
@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()

# Mock use case and repository to isolate logic
class MockPeopleRepository:
    def __init__(self, api_url, logger):
        pass

    def get_people(self, page=1):
        luke = Person("Luke Skywalker","test-height","test-mass","test-hair-color","test-skin-color","test-eye-color","test-birthday","test-gender","test-homeworld", [],[],[],[],"2014-12-10T16:20:44.310000Z","2014-12-20T21:17:50.327000Z","https://swapi.dev/api/people/11/")
        darth = Person("Darth Vader","test-height","test-mass","test-hair-color","test-skin-color","test-eye-color","test-birthday","test-gender","test-homeworld", [],[],[],[],"2014-12-10T16:20:44.310000Z","2014-12-20T21:17:50.327000Z","https://swapi.dev/api/people/11/")
        leia = Person("Leia Organa","test-height","test-mass","test-hair-color","test-skin-color","test-eye-color","test-birthday","test-gender","test-homeworld", [],[],[],[],"2014-12-10T16:20:44.310000Z","2014-12-20T21:17:50.327000Z","https://swapi.dev/api/people/11/")
        if page == 1:
            return [luke, darth]
        if page == 2:
            return [leia]
        else:
            return []

    def get_all_people(self):
        luke = Person("Luke Skywalker","test-height","test-mass","test-hair-color","test-skin-color","test-eye-color","test-birthday","test-gender","test-homeworld", [],[],[],[],"2014-12-10T16:20:44.310000Z","2014-12-20T21:17:50.327000Z","https://swapi.dev/api/people/11/")
        darth = Person("Darth Vader","test-height","test-mass","test-hair-color","test-skin-color","test-eye-color","test-birthday","test-gender","test-homeworld", [],[],[],[],"2014-12-10T16:20:44.310000Z","2014-12-20T21:17:50.327000Z","https://swapi.dev/api/people/11/")
        leia = Person("Leia Organa","test-height","test-mass","test-hair-color","test-skin-color","test-eye-color","test-birthday","test-gender","test-homeworld", [],[],[],[],"2014-12-10T16:20:44.310000Z","2014-12-20T21:17:50.327000Z","https://swapi.dev/api/people/11/")
        return [luke, leia, darth]


class MockGetPeopleUseCase:
    def __init__(self, people_repository, logger):
        self.people_repository = people_repository

    def execute(self, page=None):
        if page:
            return self.people_repository.get_people(page)
        else:
            return self.people_repository.get_all_people()


# Tests
def test_get_sorted_people_page_1(client, monkeypatch):
    monkeypatch.setattr('controllers.people_controller.PeopleRepository', MockPeopleRepository)
    monkeypatch.setattr('controllers.people_controller.GetPeopleUseCase', MockGetPeopleUseCase)

    response = client.get('/people/data?page=1')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['name'] == "Luke Skywalker"
    assert data[1]['name'] == "Darth Vader"


def test_get_sorted_people_page_2(client, monkeypatch):
    monkeypatch.setattr('controllers.people_controller.PeopleRepository', MockPeopleRepository)
    monkeypatch.setattr('controllers.people_controller.GetPeopleUseCase', MockGetPeopleUseCase)

    response = client.get('/people/data?page=2')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['name'] == "Leia Organa"


def test_get_all_people(client, monkeypatch):
    monkeypatch.setattr('controllers.people_controller.PeopleRepository', MockPeopleRepository)
    monkeypatch.setattr('controllers.people_controller.GetPeopleUseCase', MockGetPeopleUseCase)

    response = client.get('/people/data?all=true')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data) == 3
    assert data[0]['name'] == "Luke Skywalker"
    assert data[1]['name'] == "Leia Organa"
    assert data[2]['name'] == "Darth Vader"


def test_get_sorted_people_no_params(client, monkeypatch):
    monkeypatch.setattr('controllers.people_controller.PeopleRepository', MockPeopleRepository)
    monkeypatch.setattr('controllers.people_controller.GetPeopleUseCase', MockGetPeopleUseCase)

    response = client.get('/people/data')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['name'] == "Luke Skywalker"
    assert data[1]['name'] == "Darth Vader"


def test_get_sorted_people_invalid_page(client, monkeypatch):
    monkeypatch.setattr('controllers.people_controller.PeopleRepository', MockPeopleRepository)
    monkeypatch.setattr('controllers.people_controller.GetPeopleUseCase', MockGetPeopleUseCase)