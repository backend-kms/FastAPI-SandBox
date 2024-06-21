from passlib.context import CryptContext

from app.database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ResponseAnnotationHandler:

    @staticmethod
    def response_200_ok(message: str = "success"):
        return dict(
            content={"application/json": {"example": {"message": message}}},
            description="Error: Unauthorized",
        )

    @staticmethod
    def response_201_created(message: str = "success"):
        return dict(
            content={"application/json": {"example": {"message": message}}},
            description="Error: Unauthorized",
        )

    @staticmethod
    def response_204_no_content():
        return dict(
            content={"application/json": {"example": {}}},
            description="Error: Unauthorized",
        )

    @staticmethod
    def response_error(detail, description):
        return dict(
            content={"application/json": {"example": {"detail": detail}}},
            description=description,
        )

    @staticmethod
    def response_401_error():
        return dict(
            content={"application/json": {"example": {"detail": "Not authenticated"}}},
            description="Error: Unauthorized",
        )


class ResponseHandler:
    @staticmethod
    def response_200_ok(message: str = "success"):
        return dict(
            message=message,
        )

    @staticmethod
    def response_201_created(message: str = "success"):
        return dict(
            message=message,
        )


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
