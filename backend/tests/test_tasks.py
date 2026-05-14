def test_create_task_returns_201_with_valid_data(client):
    res = client.post("/api/tasks", json={"title": "테스트 업무"})
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "테스트 업무"
    assert data["status"] == "todo"
    assert "description" in data


def test_create_task_returns_400_when_title_is_missing(client):
    res = client.post("/api/tasks", json={"description": "설명만 있음"})
    assert res.status_code == 422  # FastAPI는 필수 필드 누락 시 422 반환


def test_create_task_returns_400_when_title_is_empty(client):
    res = client.post("/api/tasks", json={"title": ""})
    assert res.status_code == 422


def test_create_task_with_due_at(client):
    res = client.post("/api/tasks", json={
        "title": "마감 있는 업무",
        "due_at": "2026-05-12T18:00:00Z"
    })
    assert res.status_code == 201
    assert res.json()["due_at"] is not None


def test_list_tasks_returns_200_and_excludes_description(client):
    client.post("/api/tasks", json={"title": "업무 1"})
    client.post("/api/tasks", json={"title": "업무 2"})
    res = client.get("/api/tasks")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2
    # 목록에는 description 필드가 없어야 함
    assert "description" not in data[0]


def test_list_tasks_returns_newest_first(client):
    client.post("/api/tasks", json={"title": "첫 번째"})
    client.post("/api/tasks", json={"title": "두 번째"})
    res = client.get("/api/tasks")
    assert res.json()[0]["title"] == "두 번째"


def test_get_task_returns_200_with_description(client):
    created = client.post("/api/tasks", json={
        "title": "단건 조회 업무",
        "description": "상세 설명"
    }).json()
    res = client.get(f"/api/tasks/{created['id']}")
    assert res.status_code == 200
    assert res.json()["description"] == "상세 설명"


def test_get_task_returns_404_when_id_not_found(client):
    res = client.get("/api/tasks/99999")
    assert res.status_code == 404


def test_update_task_returns_200_with_partial_update(client):
    created = client.post("/api/tasks", json={"title": "수정 전"}).json()
    res = client.put(f"/api/tasks/{created['id']}", json={"status": "in_progress"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "in_progress"
    assert data["title"] == "수정 전"  # 기존 필드 유지


def test_update_task_returns_404_when_id_not_found(client):
    res = client.put("/api/tasks/99999", json={"status": "done"})
    assert res.status_code == 404


def test_delete_task_returns_204(client):
    created = client.post("/api/tasks", json={"title": "삭제할 업무"}).json()
    res = client.delete(f"/api/tasks/{created['id']}")
    assert res.status_code == 204


def test_delete_task_returns_404_when_id_not_found(client):
    res = client.delete("/api/tasks/99999")
    assert res.status_code == 404


def test_deleted_task_not_in_list(client):
    created = client.post("/api/tasks", json={"title": "삭제 후 목록 확인"}).json()
    client.delete(f"/api/tasks/{created['id']}")
    res = client.get("/api/tasks")
    ids = [t["id"] for t in res.json()]
    assert created["id"] not in ids
