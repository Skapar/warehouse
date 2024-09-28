from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str
    email: EmailStr = Field(..., example="john.doe@example.com")

    role_id: int


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

class UserUpdate(BaseModel):
    name: str | None
    email: EmailStr | None
    role_id: int | None
    password: str | None
