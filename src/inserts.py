import sqlite3
import uuid

from werkzeug.security import generate_password_hash

password = 'admin:sy.jem'
hashed_password = generate_password_hash(password)
user_id = str(uuid.uuid4())

conn = sqlite3.connect('src/instance/app.db')

conn.execute(
    """
    INSERT INTO users (id, first_name, last_name, email, role)
    VALUES (?, ?, ?, ?, ?);
    """,
    (user_id, 'Jemuel', 'Repoylo', 'syjem143@gmail.com', 'admin')
)

conn.execute(
    """
    INSERT INTO passwords (user_id, current_password_hash)
    VALUES (?, ?);
    """,
    (user_id, hashed_password)
)

conn.commit()
conn.close()
