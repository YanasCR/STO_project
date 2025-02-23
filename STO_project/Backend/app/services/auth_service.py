from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from passlib.hash import bcrypt

def register_user(user: UserCreate, db: Session):
    hashed_password = bcrypt.hash(user.password)
    db_user = User(email=user.email, password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User created", "email": db_user.email}
