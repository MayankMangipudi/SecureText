from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from app.database import Base
from datetime import datetime

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    algorithm = Column(String)
    input_length = Column(Integer)
    plaintext_preview = Column(Text)  # Store first 100 chars of plaintext
    timestamp = Column(DateTime, default=datetime.utcnow)
