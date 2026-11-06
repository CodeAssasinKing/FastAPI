from sqlalchemy import String, Boolean

from models.defaults import Base, pk, created_at, updated_at
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import sqlalchemy as sa

class User(Base):
    __tablename__ = "user"
    pk : Mapped[pk]
    username : Mapped[str] = mapped_column(String(length=255), index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(length=255), nullable=False)
    admin: Mapped[bool] = mapped_column(Boolean, index=True, default=False, server_default=sa.false())
    banned: Mapped[bool] = mapped_column(Boolean, index=True, default=False, server_default=sa.false())
    updated_at: Mapped[updated_at]
    created_at: Mapped[created_at]