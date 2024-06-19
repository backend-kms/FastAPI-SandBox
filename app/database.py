import datetime
from typing import Optional

from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.sql import func

import config


class Base(DeclarativeBase):
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))


SQLALCHEMY_DATABASE_URL = config.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLALCHEMY_DATABASE_URL: 데이터베이스 접속 주소
# SessionLocal: 데이터베이스에 접속하기 위해 필요한 클래스
#   autocommit=False: 데이터를 변경했을 때 commit이라는 사인을 주어야만 실제 저장이 된다.
#   autoflush: 세션 내에서 여러 작업을 수행한 후 flush()를 호출하여 데이터베이스에 변경 사항을 기록한다.
#   bind: 세션이 특정 데이터베이스 엔진과 연결되도록 설정한다.
