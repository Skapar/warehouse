from pydantic import BaseModel

class RoleBase(BaseModel):
    title: str


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: int
