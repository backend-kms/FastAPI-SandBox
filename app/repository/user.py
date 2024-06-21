# 3. repository: 데이터베이스와의 상호작용을 처리, CRUD를 처리하는 곳

from sqlalchemy.orm import Session

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

    def check_existing_email(user: model.user.UserCreate, db: Session):
        return db.query(User).filter((User.email == user.email)).first()
