def test_create_experience(client, test_token_1):
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token_1}"}

    response = client.post(
        "/experiences",
        json={
            "title": "Beach",
            "description": "A sunny day",
            "location": "Costa Brava",
            "lat": 12.58658855,
            "lon": 54.39338383,
            "rating": 5,
        },
    )

    assert response.status_code == 201


def test_update_experience(client, test_experience_1, test_token_1):
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token_1}"}

    response = client.put(
        f"/experiences/{test_experience_1['experience_id']}",
        json={
            "experience_id": test_experience_1["experience_id"],
            "title": test_experience_1["title"],
            "description": test_experience_1["description"],
            "location": test_experience_1["location"],
            "lat": test_experience_1["lat"],
            "lon": test_experience_1["lon"],
            "rating": 4},
    )

    assert response.status_code == 200
    assert response.json()["rating"] == 4


def test_update_experience_unauthorized(client, test_experience_1, test_token_2, test_token_1, test_user_1, test_user_2):
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token_2}"}

    response = client.put(
        f"/experiences/{test_experience_1['experience_id']}",
        json={
            "experience_id": test_experience_1["experience_id"],
            "title": test_experience_1["title"],
            "description": test_experience_1["description"],
            "location": test_experience_1["location"],
            "lat": test_experience_1["lat"],
            "lon": test_experience_1["lon"],
            "rating": 4},
    )

    assert response.status_code == 403


def test_delete_experience(client, test_experience_1, test_token_1):
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token_1}"}

    response = client.delete(f"/experiences/{test_experience_1['experience_id']}")

    assert response.status_code == 200


def test_delete_experience_unauthorized(client, test_experience_1, test_token_2):
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token_2}"}

    response = client.delete(f"/experiences/{test_experience_1['experience_id']}")

    assert response.status_code == 403
