from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app import model
from app.repository.user import UserRepository
from app.service.user import UserService
from app.utils import ResponseAnnotationHandler, get_db, oauth2_scheme

router = APIRouter(prefix="/admin")


@router.get(
    path="/users",
    tags=["admin"],
    summary="사용자 목록",
    response_model=Page[model.user.UserListItem],
    responses={
        401: ResponseAnnotationHandler.response_401_error(),
        400: ResponseAnnotationHandler.response_error(
            detail="유효하지 않은 토큰입니다.",
            description="토큰 유효성 에러",
        ),
    },
)
def users_profile(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> Page[model.user.UserList]:
    UserRepository.check_access_token_validation(token, db)
    valid_users = UserService.get_users(db=db)
    return paginate(valid_users)
