from pydantic import BaseModel

class JournalEntry(BaseModel):
    user_id: int
    message: str
    date: str
    hide_yn: bool
    time: str

class MoodEntry(BaseModel):
    user_id: int
    mood: str
    date: str
    description: str

class GratitudeEntry(BaseModel):
    date: str
    comment: str