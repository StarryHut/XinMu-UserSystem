from pydantic import BaseModel
import typing


class UpdateUserById(BaseModel):
    uid: int
    username: str
    password: typing.Union[str, int]
    role: str
