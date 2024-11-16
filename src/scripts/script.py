import uuid
import json
from werkzeug.security import generate_password_hash
from models import db, Users, Passwords

# Load user data from JSON file
with open('users.json', 'r') as f:
    users_data = json.load(f)


def add_users_to_db(users_data):
    for user_data in users_data:
        # Split the name into first_name and last_name
        first_name, last_name = user_data['name'].split(' ', 1)

        # Generate unique user ID
        user_id = str(uuid.uuid4())

        # Create new user record
        user = Users(
            id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=user_data['email'],
            avatar=user_data['avatar'],
            role='user',
        )

        db.session.add(user)

        # Create a password instance
        password = Passwords(
            user_id=user.id,
            current_password_hash=generate_password_hash(user_data['password'])
        )

        db.session.add(password)

    db.session.commit()
    print("Users and passwords added successfully.")


if __name__ == "__main__":
    from app import app

    with app.app_context():
        add_users_to_db(users_data)
