from .base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import (
    String,
    ForeignKey,
    Integer,
    DateTime,
    func,
    CheckConstraint,
)


class Order(Base):
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL")
    )

    user: Mapped["User"] = relationship("User")
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
    )
