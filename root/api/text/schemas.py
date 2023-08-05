from pydantic import BaseModel
from datetime import date


class STranslate(BaseModel):
    source_text: str
    target_language: str
    translated_text: str
    create_date: date
    last_access_date: date
