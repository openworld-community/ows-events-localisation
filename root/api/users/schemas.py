from pydantic import BaseModel
from datetime import date


class SUsers(BaseModel):
    username: str
    password_hash: str
    create_date: date
    last_access_date: date

