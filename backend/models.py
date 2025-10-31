from pydantic import BaseModel

class LogRequest(BaseModel):
    message: str
    source: str