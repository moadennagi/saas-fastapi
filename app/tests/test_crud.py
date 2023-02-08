from database import User

def test_get_record(user, test_database):
    res = test_database.query(User)
