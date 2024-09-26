from .base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import (
    String,
    ForeignKey,
    Integer,
    Column,
    DECIMAL,
    DateTime,
    func,
    CheckConstraint,
)

class Role(Base):
    title: Mapped[str] = mapped_column(unique=True)

    # user_roles: Mapped[list["UserRole"]] = relationship(
    #     "UserRole", back_populates="role"
    # )

    # users: Mapped[list["User"]] = relationship(
    #     "User", secondary="user_roles", back_populates="roles"
    # )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )