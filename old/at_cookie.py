

# External imports
from pydantic import BaseModel


class ATCookies(BaseModel):
    session_id: str
    session_data: str

