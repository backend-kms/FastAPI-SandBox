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
    age: str
