from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.history import History
from backend.app.models.user import User
from backend.app.schemas.history_schema import HistoryOut
from backend.app.utils.jwt_handler import create_access_token
import jwt
from backend.config import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from typing import List

router = APIRouter(prefix="/history")
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(401, "Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(401, "User not found")
    return user

@router.get("/list", response_model=List[HistoryOut])
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    history = db.query(History).filter(History.user_id == current_user.id).order_by(History.timestamp.desc()).all()
    return history

@router.delete("/clear")
def clear_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.query(History).filter(History.user_id == current_user.id).delete()
    db.commit()
    return {"message": "History cleared successfully"}

@router.post("/add")
def add_history(algorithm: str, input_length: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_history = History(
        user_id=current_user.id,
        algorithm=algorithm,
        input_length=input_length
    )
    db.add(new_history)
    db.commit()
    return {"message": "History added successfully"}