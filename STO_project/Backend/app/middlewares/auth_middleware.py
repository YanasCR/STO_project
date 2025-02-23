from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from database import get_db
from app.models.user import User
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# Используем HTTP Bearer Token (токен в заголовке Authorization)
security = HTTPBearer()

# Функция для генерации JWT-токена
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Функция для декодирования токена

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="❌ Токен истек")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="❌ Недействительный токен")


# Middleware для аутентификации пользователей
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="❌ Недействительный токен")

    user = db.query(User).filter(User.email == payload["sub"]).first()
    if user is None:
        raise HTTPException(status_code=401, detail="❌ Пользователь не найден")

    return user
