# 1. routers: API 엔드포인트를 정의, 각 엔드포인트는 클라이언트와의 상호작용을 처리

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app import model
from app.repository.user import UserRepository
from app.service.user import UserService
from app.utils import ResponseAnnotationHandler, ResponseHandler, get_db, oauth2_scheme

router = APIRouter(prefix="/user")


@router.post(
    path="/sign-up",
    tags=["user"],
    summary="회원가입",
    status_code=201,
    responses={
        201: ResponseAnnotationHandler.response_201_created(
            message="회원가입이 완료되었습니다.",
        ),
        409: ResponseAnnotationHandler.response_error(
            detail="이미 존재하는 사용자입니다.",
            description="아이디 중복 에러",
        ),
    },
)
def sign_up(user: model.user.UserCreate, db: Session = Depends(get_db)):
    UserService.sign_up(user, db)
    return True


@router.post(
    path="/sign-in",
    tags=["user"],
    summary="로그인",
    response_model=model.user.UserToken,
    responses={
        400: ResponseAnnotationHandler.response_error(
            detail="아이디와 비밀번호를 확인하세요.",
            description="로그인 에러",
        )
    },
)
def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    login_info = UserService.sign_in(user=form_data, db=db)
    return model.user.UserToken(**login_info)


@router.delete(
    path="/sign-out",
    tags=["user"],
    summary="로그아웃",
    status_code=204,
    responses={
        204: ResponseAnnotationHandler.response_204_no_content(),
        401: ResponseAnnotationHandler.response_401_error(),
        400: ResponseAnnotationHandler.response_error(
            detail="유효하지 않은 토큰입니다.", description="토큰 유효성 에러"
        ),
    },
)
def sign_out(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    UserService.sign_out(token=token, db=db)


@router.get(
    path="/profile",
    tags=["user"],
    summary="내 정보",
    response_model=model.user.UserProfile,
    responses={
        401: ResponseAnnotationHandler.response_401_error(),
        400: ResponseAnnotationHandler.response_error(
            detail="유효하지 않은 토큰입니다.",
            description="토큰 유효성 에러",
        ),
    },
)
def user_profile(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    UserRepository.check_access_token_validation(token, db)
    user = UserService.get_user_profile(token=token, db=db)

    return model.user.UserProfile(**user)
