from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from app.models import User, Wallet
from app.database import Base
from app.dependency import get_db
from main import app

DATABASE_URS = "sqlite:///./test.db"

test_engine = create_engine(DATABASE_URS, connect_args={"check_same_thread": False})

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def get_test_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db

@pytest.fixture()
def client():
    yield TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture

def test_user(db_session):
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    return user
@pytest.fixture
def test_wallet(db_session, test_user):
    wallet = Wallet(name="card", balance=200, user_id=test_user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)
    return wallet