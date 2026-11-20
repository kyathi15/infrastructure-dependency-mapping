
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    from app.database.connection import Base, engine

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


def add_sample_components():
    components = [
        {
            "id": "db1",
            "name": "Main Database",
            "type": "database",
            "criticality": "critical",
        },
        {
            "id": "login1",
            "name": "Login Service",
            "type": "service",
            "criticality": "high",
        },
        {
            "id": "portal1",
            "name": "User Portal",
            "type": "application",
            "criticality": "high",
        },
    ]

    for component in components:
        response = client.post("/components", json=component)
        assert response.status_code == 201


def test_create_and_list_components():
    add_sample_components()

    response = client.get("/components")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_create_dependency():
    add_sample_components()

    response = client.post(
        "/dependencies",
        json={"source_id": "db1", "target_id": "login1"},
    )

    assert response.status_code == 201


def test_prevent_duplicate_dependency():
    add_sample_components()

    dependency = {"source_id": "db1", "target_id": "login1"}

    first_response = client.post("/dependencies", json=dependency)
    second_response = client.post("/dependencies", json=dependency)

    assert first_response.status_code == 201
    assert second_response.status_code == 400


def test_prevent_circular_dependency():
    add_sample_components()

    client.post(
        "/dependencies",
        json={"source_id": "db1", "target_id": "login1"},
    )

    client.post(
        "/dependencies",
        json={"source_id": "login1", "target_id": "portal1"},
    )

    response = client.post(
        "/dependencies",
        json={"source_id": "portal1", "target_id": "db1"},
    )

    assert response.status_code == 400


def test_failure_impact_analysis():
    add_sample_components()

    client.post(
        "/dependencies",
        json={"source_id": "db1", "target_id": "login1"},
    )

    client.post(
        "/dependencies",
        json={"source_id": "login1", "target_id": "portal1"},
    )

    response = client.post("/simulate-failure/db1")

    assert response.status_code == 200
    assert response.json()["total_affected"] == 2


def test_unknown_component_failure():
    response = client.post("/simulate-failure/unknown")

    assert response.status_code == 404
