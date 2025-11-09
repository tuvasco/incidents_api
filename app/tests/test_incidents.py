# app/tests/test_incidents.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core import database  # импортируем сам модуль, чтобы заменить внутри него engine и SessionLocal
from app.main import app

# Используем in-memory SQLite, общую для всех соединений
TEST_DATABASE_URL = "sqlite:///:memory:"

# Создаём общий engine для тестов
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Создаём новую SessionLocal, связанную с тестовым engine
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 ВАЖНО: подменяем реальные объекты в модуле app.core.database
database.engine = engine
database.SessionLocal = TestingSessionLocal
database.Base.metadata.bind = engine


# Переопределяем зависимость get_db для FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[database.get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def prepare_db():
    """Создаёт таблицы перед каждым тестом."""
    database.Base.metadata.drop_all(bind=engine)
    database.Base.metadata.create_all(bind=engine)
    yield
    database.Base.metadata.drop_all(bind=engine)


def test_create_and_get_incident():
    payload = {"description": "Тест инцидента", "source": "operator"}
    r = client.post("/incidents/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["description"] == payload["description"]
    assert data["status"] == "new"

    # Проверяем, что GET возвращает инцидент
    r2 = client.get("/incidents/")
    items = r2.json()
    assert len(items) == 1
    assert items[0]["description"] == "Тест инцидента"


def test_update_status_404():
    r = client.patch("/incidents/9999", json={"status": "closed"})
    assert r.status_code == 404
