from fastapi.testclient import TestClient

from ..app.main import app

client = TestClient(app)

def test_upload_file():
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"Test file content")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "uid" in data

def test_get_file():
    # Сначала загрузим файл
    upload_response = client.post(
        "/upload",
        files={"file": ("test.txt", b"Test file content")}
    )
    uid = upload_response.json()["uid"]

    # Затем попытаемся его получить
    response = client.get(f"/files/{uid}")
    assert response.status_code == 200
    assert response.content == b"Test file content"
