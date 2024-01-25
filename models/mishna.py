from typing import List
from pydantic import BaseModel

class Mishna(BaseModel):
    chapter: str
    mishna: str
    tags: List[str]
    text: str