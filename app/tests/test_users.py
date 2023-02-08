import pytest
from sqlalchemy import text
from schemas import PydanticCreateUser
from models import User


def test_user_role(role, user, test_database):
    user.roles.append(role)
    test_database.add(user)
    test_database.commit()

    stmt = text('SELECT role_id FROM users_roles WHERE user_id = :id')
    res = test_database.execute(stmt, {'id': user.id}).fetchone()
    assert res.role_id == role.id


def test_user_permissions(role, user, permissions):
    role.permissions = permissions
    user.roles.append(role)

    assert user.permissions
    for perm in zip(user.permissions, permissions):
        assert perm[0][0] == perm[1].resource
        assert perm[0][1] == perm[1].action


def test_user_not_enough_permissions(role, user, permissions):
    role.permissions = permissions
    user.roles.append(role)

    with pytest.raises(PermissionError, match='Not enough permissions'):
        user.has_permissions([('users', 'delete')])


def test_create_user_with_role(test_database, role):
    user_pydantic = PydanticCreateUser(username='foo', password='foo',
                                       role_id=role.id)
    obj = User.create(test_database, data=user_pydantic)
    assert role in obj.roles
