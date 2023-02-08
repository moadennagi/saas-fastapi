import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, Role, Permission, User # noqa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings


engine = create_engine(settings.test_database_url)
SessionMaker = sessionmaker(engine)


@pytest.fixture(scope='module')
def client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope='module')
def test_database(init_db):
    try:
        db = SessionMaker()
        yield db
    finally:
        db.close()


@pytest.fixture(scope='session')
def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='module')
def role(test_database):
    role = Role(name='admin')
    test_database.add(role)
    test_database.commit()
    yield role

    test_database.delete(role)
    test_database.commit()


@pytest.fixture(scope='module')
def user(test_database):
    user = User(username='admin', password='admin')
    test_database.add(user)
    test_database.commit()
    yield user

    test_database.delete(user)
    test_database.commit()


@pytest.fixture(scope='module')
def permissions(test_database):
    permissions = []
    for permission_tuple in [('users', 'read'), ('users', 'create'), ('users', 'update')]:
        permissions.append(Permission(resource=permission_tuple[0], action=permission_tuple[1]))
    test_database.add_all(permissions)
    test_database.commit()
    yield permissions

    for perm in permissions:
        test_database.delete(perm)
    test_database.commit()
