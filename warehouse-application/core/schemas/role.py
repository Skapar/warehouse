from pydantic import BaseModel, validator


class RoleBase(BaseModel):
    title: str

    @validator("title", pre=True, always=True)
    def title_must_be_uppercase(cls, value: str) -> str:
        if value:
            return value.upper()
        return value


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: int
