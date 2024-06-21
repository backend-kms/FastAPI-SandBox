# 4. model: 데이터 스키마를 정의, 주로 데이터 유효성 검사와 직렬화, 비직렬화를 담당

import datetime
from typing import List, Literal, Optional

from pydantic import UUID4, BaseModel, NaiveDatetime


# 흐름 1. model: schema 작성
class UserCreate(BaseModel):
    email: str
    password: str
    username: str
    gender: Literal["male", "female"]
    age: int


class UserToken(BaseModel):
    access_token: str
    username: str


class User(BaseModel):
    id: UUID4
    email: str
    password: str
    username: str
    gender: str
    age: str
    role: str
    created_at: NaiveDatetime
    updated_at: NaiveDatetime
    last_login: NaiveDatetime
