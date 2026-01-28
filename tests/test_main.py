from fastapi.testclient import TestClient


# def test_create_item_success(client):
#     response = client.post(
#         "/items",
#         json = {"name":"docker", "description":"container"}
#     )

#     assert response.status_code == 201
#     data = response.json()
#     assert data["name"] == "docker"
#     assert data["description"] == "container"

def test_create_item_validation_error(client):
    response = client.post(
        "/items",
        json={"name": "", "description": "fail"}
    )

    assert response.status_code == 422