from pydantic import BaseModel


class profile(BaseModel):
    name: str
    tittle: str
    bio: str
    email: str
    is_human: bool
