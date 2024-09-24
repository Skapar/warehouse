from .base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

class User(Base):
    username: Mapped[str] = mapped_column(unique=True)