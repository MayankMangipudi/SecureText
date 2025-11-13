from pydantic import BaseModel, ConfigDict
from datetime import datetime

class HistoryOut(BaseModel):
    id: int
    algorithm: str
    input_length: int
    plaintext_preview: str  
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)
