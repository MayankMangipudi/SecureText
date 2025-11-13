from pydantic import BaseModel

class TextPayload(BaseModel):
    text: str
    key: str | None = None
    public_key: str | None = None
    private_key: str | None = None
