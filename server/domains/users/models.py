from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from common.base_model import Base, TimestampMixin, UUIDMixin
from domains.users.enums import UserRole


class User(Base, UUIDMixin, TimestampMixin):
    """User database model leveraging base mixins for UUIDs and timestamps."""
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(String(50), default=UserRole.USER, nullable=False)