"""Create (or update) a login user for the dashboard.

Run: python create_user.py <username> <password> ["Full Name"] [role]
"""
import sys

from app.core.security import hash_password
from app.database.session import Base, SessionLocal, engine
from app.models import User


def main():
    if len(sys.argv) < 3:
        print("Usage: python create_user.py <username> <password> [full_name] [role]")
        sys.exit(1)

    username, password = sys.argv[1], sys.argv[2]
    full_name = sys.argv[3] if len(sys.argv) > 3 else username
    role = sys.argv[4] if len(sys.argv) > 4 else "risk_analyst"

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            user.hashed_password = hash_password(password)
            user.full_name = full_name
            user.role = role
        else:
            user = User(username=username, hashed_password=hash_password(password), full_name=full_name, role=role)
            db.add(user)
        db.commit()
        print(f"User '{username}' ready.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
