from pydantic import BaseModel
import typing


class Register(BaseModel):
    username: typing.Union[str, int]
    password: typing.Union[str, int]
    role: str


class Login(BaseModel):
    username: typing.Union[str, int]
    password: typing.Union[str, int]
