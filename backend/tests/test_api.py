import jwt
import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import app

SECRET = "x" * 40


def _client(secret: str = "", env: str = "development") -> TestClient:
    app.dependency_overrides[get_settings] = lambda: Settings(
        supabase_jwt_secret=secret, app_env=env, _env_file=None)
    return TestClient(app)


@pytest.fixture(autouse=True)
def _reset():
    yield
    app.dependency_overrides.clear()


def test_health():
    assert _client().get("/health").json() == {"status": "ok"}


def test_labs_dev_bypass():
    r = _client().post("/v1/labs/evaluate", json={"sex": "male", "hemoglobin_gdl": 11})
    assert r.status_code == 200
    body = r.json()
    assert body["findings"][0]["category"] == "Mild anemia"
    assert "not a diagnosis" in body["disclaimer"]


def test_labs_requires_token_when_secret_set():
    assert _client(SECRET).post("/v1/labs/evaluate", json={}).status_code == 401


def test_labs_rejects_bad_token():
    r = _client(SECRET).post("/v1/labs/evaluate", json={},
                             headers={"Authorization": "Bearer nope"})
    assert r.status_code == 401


def test_labs_accepts_valid_token():
    tok = jwt.encode({"sub": "u1", "aud": "authenticated"}, SECRET, algorithm="HS256")
    r = _client(SECRET).post("/v1/labs/evaluate", json={"sbp": 150, "dbp": 95},
                             headers={"Authorization": f"Bearer {tok}"})
    assert r.status_code == 200


def test_auth_not_bypassed_in_production_without_secret():
    r = _client("", env="production").post("/v1/labs/evaluate", json={})
    assert r.status_code == 500


def test_input_validation():
    assert _client().post("/v1/labs/evaluate", json={"sbp": 5}).status_code == 422


def test_xray_rejects_wrong_type():
    r = _client().post("/v1/imaging/xray", files={"file": ("a.txt", b"hi", "text/plain")})
    assert r.status_code == 415
