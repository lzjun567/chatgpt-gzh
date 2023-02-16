from .base import BaseModel


class SignatureDto(BaseModel):
    signature: str
    echostr: str
    timestamp: str
    nonce: str
