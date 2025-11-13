from pydantic import BaseModel

class AesVisualizeRequest(BaseModel):
    plaintext: str
    key: str

class RsaVisualizeRequest(BaseModel):
    plaintext: str