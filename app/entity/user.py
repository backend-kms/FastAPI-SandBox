from __future__ import annotations

import datetime
import uuid
from typing import List, Optional

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)  # uuid
    email: Mapped[str] = mapped_column(unique=True)  # 이메일
    password: Mapped[str] = mapped_column(String(length=128))  # 패스워드
    username: Mapped[str] = mapped_column(String(length=20))  # 이름
    gender: Mapped[str] = mapped_column(String(length=6))  # 성별
    age: Mapped[int] = mapped_column(default=0)  # 나이
    role: Mapped[str] = mapped_column(String(length=20))  # 역할
    last_login: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True)
    )  # 마지막 로그인

    # Relationship
    user_token: Mapped["UserToken"] = relationship(
        back_populates="user",
    )


class UserToken(Base):
    __tablename__ = "user_token"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id"),
    )
    token: Mapped[Optional[str]]

    # Relationship
    user: Mapped["User"] = relationship(
        back_populates="user_token",
        cascade="delete",
        uselist=False,
    )
