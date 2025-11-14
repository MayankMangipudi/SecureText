from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.crypto_schema import TextPayload
from app.security.aes_lib import aes_encrypt, aes_decrypt, generate_aes_key
from app.security.rsa_lib import rsa_encrypt, rsa_decrypt, generate_rsa_keys
from app.security.sha_lib import sha256_hash
from app.database import SessionLocal
from app.models.user import User
from app.models.history import History
import jwt
from backend.config import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

router = APIRouter(prefix="/crypto")
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

def log_history(db: Session, user_id: int, algorithm: str, input_text: str):
    # Store first 100 characters as preview
    preview = input_text[:100] if len(input_text) > 100 else input_text
    history = History(
        user_id=user_id, 
        algorithm=algorithm, 
        input_length=len(input_text),
        plaintext_preview=preview
    )
    db.add(history)
    db.commit()

# ---------- AES ----------
@router.post("/aes/encrypt")
def aes_encrypt_route(payload: TextPayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        result = aes_encrypt(payload.text, payload.key)
        log_history(db, current_user.id, "AES-Encrypt", payload.text)
        return {"ciphertext": result}
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/aes/decrypt")
def aes_decrypt_route(payload: TextPayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        result = aes_decrypt(payload.text, payload.key)
        log_history(db, current_user.id, "AES-Decrypt", payload.text)
        return {"plaintext": result}
    except Exception as e:
        raise HTTPException(400, str(e))


@router.get("/aes/generate_key")
def aes_key_gen(current_user: User = Depends(get_current_user)):
    return {"key": generate_aes_key()}


# ---------- RSA ----------
@router.get("/rsa/generate_keys")
def rsa_key_gen(current_user: User = Depends(get_current_user)):
    private_key, public_key = generate_rsa_keys()
    return {"private_key": private_key, "public_key": public_key}


@router.post("/rsa/encrypt")
def rsa_encrypt_route(payload: TextPayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not payload.public_key:
        raise HTTPException(400, "Public key required")
    try:
        result = rsa_encrypt(payload.text, payload.public_key)
        log_history(db, current_user.id, "RSA-Encrypt", payload.text)
        return {"ciphertext": result}
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/rsa/decrypt")
def rsa_decrypt_route(payload: TextPayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not payload.private_key:
        raise HTTPException(400, "Private key required")
    try:
        result = rsa_decrypt(payload.text, payload.private_key)
        log_history(db, current_user.id, "RSA-Decrypt", payload.text)
        return {"plaintext": result}
    except Exception as e:
        raise HTTPException(400, str(e))


# ---------- SHA-256 ----------
@router.post("/sha256/hash")
def sha_hash(payload: TextPayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = sha256_hash(payload.text)
    log_history(db, current_user.id, "SHA256-Hash", payload.text)
    return {"hash": result}
