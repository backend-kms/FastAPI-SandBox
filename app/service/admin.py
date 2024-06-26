# 2. service: 비지니스 로직을 처리, 유효성 검사, 직렬화 및 비직렬화, db 연결을 제외한 모든 처리 / 데이터베이스와의 직접적인 상호작용은 없음

from sqlalchemy.orm import Session

from app import model
from app.enums import UserGender, UserRole
from app.repository.user import UserRepository
from app.utils import pwd_context


class AdminUserService:
    @staticmethod
    def get_users(db: Session):
        return [
            model.user.UserListItem(
                email=db_user.email,
                username=db_user.username,
                gender=UserGender[db_user.gender.upper()].display,
                age=db_user.age,
                role=UserRole[db_user.role.upper()].display,
                last_login=db_user.last_login,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at,
                deleted_at=db_user.deleted_at,
            )
            for db_user in UserRepository.get_users(db)
        ]
