from typing import Optional

from pydantic import BaseModel


class Place(BaseModel):
    name: str
    type: str
    address: str
    why: str
    price_range: Optional[str] = None
    rating: Optional[float] = None
    dress_code: Optional[str] = None
