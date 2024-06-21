# 3. repository: 데이터베이스와의 상호작용을 처리, CRUD를 처리하는 곳
import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import model
from app.entity.user import User, UserToken
from app.enums import UserRole


class UserRepository:
    @staticmethod
    def create_user(user: model.user.UserCreate, db: Session):
        db_user = User(
            email=user.email,
            password=user.password,
            username=user.username,
            gender=user.gender,
            age=user.age,
            role=UserRole.BASIC.value,
        )
        db.add(db_user)
        user_token = UserToken(user=db_user)
        db.add(user_token)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def check_existing_email(user: model.user.UserCreate, db: Session):
        return db.query(User).filter((User.email == user.email)).first()

    @staticmethod
    def get_user_by_email(email: str, db: Session):
        return db.query(User).filter((User.email == email)).first()

    @staticmethod
    def update_last_login(user: model.user.User, access_token: str, db: Session):
        db_user = db.query(User).filter(User.email == user.email).first()

        db_user.last_login = datetime.datetime.now()
        db_user.user_token.token = access_token
        db.commit()

    @staticmethod
    def get_user_by_token(access_token: str, db: Session):
        return db.query(User).join(UserToken).filter(UserToken.token == access_token).first()

    @staticmethod
    def remove_access_token(access_token: str, db: Session):
        db_token = db.query(UserToken).filter(UserToken.token == access_token).first()
        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="유효하지 않은 토큰입니다.",
            )
        db_token.token = None
        db.commit()

    @staticmethod
    def check_access_token_validation(access_token: str, db: Session):
        db_token = db.query(UserToken).filter(UserToken.token == access_token).first()
        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="유효하지 않은 토큰입니다.",
            )
