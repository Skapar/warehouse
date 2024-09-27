from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str

    role_id: int


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
