from sqlalchemy import text


def test_database_session(test_database):
    stmt = text('SELECT * FROM users')
    res = test_database.execute(stmt)
    assert res
