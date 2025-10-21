# db.py
# simple SQLAlchemy + MariaDB setup for assignment 05
from sqlalchemy import (
    create_engine, Column, Integer, String, TIMESTAMP, func, select, update
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError

# connection settings (match docker-compose)
DB_URL = "mysql+pymysql://dbuser:dbpass@127.0.0.1:3306/studentdb"

engine = create_engine(DB_URL, pool_size=3, max_overflow=5, pool_pre_ping=True, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    fullname = Column(String(100))
    created = Column(TIMESTAMP, server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}>"

def get_all_users():
    with Session() as s:
        return s.scalars(select(User)).all()

def find_user(username):
    with Session() as s:
        return s.scalar(select(User).where(User.username == username))

def add_user(username, email, fullname=None):
    with Session() as s:
        user = User(username=username, email=email, fullname=fullname)
        s.add(user)
        try:
            s.commit()
            print(f"✅ Added: {username}")
            return user
        except IntegrityError:
            s.rollback()
            print("⚠️  Username or email already exists.")
            return None

def update_user(user_id, **fields):
    with Session() as s:
        res = s.execute(update(User).where(User.id == user_id).values(**fields))
        s.commit()
        if res.rowcount:
            print(f"🔁 Updated user id={user_id}")
        else:
            print("No matching user to update.")
