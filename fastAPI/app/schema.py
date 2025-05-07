from pydantic import BaseModel
from datetime import datetime

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteOut(NoteCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
