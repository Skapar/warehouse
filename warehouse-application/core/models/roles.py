from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    DateTime,
    func,
)


class Role(Base):
    title: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
