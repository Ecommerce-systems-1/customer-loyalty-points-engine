import pytest
from backend.database import get_connection, init_db


@pytest.fixture
def db(tmp_path):
    conn = get_connection(str(tmp_path / "test.db"))
    init_db(conn)
    conn.execute("INSERT INTO customers(id,name,email,tier,lifetime_points_earned,created_at) VALUES('C001','Test User','t@e.com','Bronze',0,'2024-01-01T00:00:00Z')")
    conn.commit()
    yield conn
    conn.close()