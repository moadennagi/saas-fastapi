from database import User
from schemas import CreateUser, UpdateUser


def test_get_record(user, test_database):
    res = User.get(test_database, pk=user.id)
    assert res.id == user.id


def test_update_record(user, test_database):
    data = UpdateUser(password='updated')
    res = User.update(test_database, pk=user.id, data=data)

    obj = test_database.query(User).filter(User.id == user.id).first()
    assert obj.password == res.password

