from fastapi.testclient import TestClient

import main


def seed_database(tmp_path, monkeypatch, rows):
    monkeypatch.setattr(main, "DATABASE_PATH", tmp_path / "registros.db")
    main.initialize_database()
    with main.get_connection() as connection:
        connection.executemany(
            "INSERT INTO records (usuario, version, fecha) VALUES (?, ?, ?)",
            [(usuario, version, "2026-08-21T00:00:00+00:00") for usuario, version in rows],
        )


def test_records_exists_returns_true_for_existing_combination(tmp_path, monkeypatch):
    seed_database(tmp_path, monkeypatch, [("ana", "1.0")])

    with TestClient(main.app) as client:
        response = client.get(
            "/records/exists", params={"usuario": "ana", "version": "1.0"}
        )

    assert response.status_code == 200
    assert response.json() == {"exists": True}


def test_records_exists_returns_false_for_missing_combination(tmp_path, monkeypatch):
    seed_database(tmp_path, monkeypatch, [("ana", "1.0")])

    with TestClient(main.app) as client:
        response = client.get(
            "/records/exists", params={"usuario": "ana", "version": "2.0"}
        )

    assert response.status_code == 200
    assert response.json() == {"exists": False}


def test_records_exists_rejects_empty_or_missing_parameters(tmp_path, monkeypatch):
    seed_database(tmp_path, monkeypatch, [])

    with TestClient(main.app) as client:
        missing_usuario = client.get("/records/exists", params={"version": "1.0"})
        missing_version = client.get("/records/exists", params={"usuario": "ana"})
        empty_usuario = client.get(
            "/records/exists", params={"usuario": "", "version": "1.0"}
        )

    assert missing_usuario.status_code == 422
    assert missing_version.status_code == 422
    assert empty_usuario.status_code == 422
