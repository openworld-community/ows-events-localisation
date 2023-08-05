from pydantic import BaseModel
from datetime import date


class SCategory(BaseModel):
    source_text: str
    category_text: str
    create_date: str
    last_access_date: date
