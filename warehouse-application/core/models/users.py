from .base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import (
    String,
    ForeignKey,
    Integer,
    DateTime,
    func,
)

from .roles import Role


class User(Base):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("role.id"))
    role: Mapped["Role"] = relationship("Role")

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
