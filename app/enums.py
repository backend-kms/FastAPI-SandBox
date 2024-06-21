from enum import Enum


class UserRole(Enum):
    BASIC = "basic"
    MANAGER = "manager"

    @property
    def display(self):
        return {
            UserRole.BASIC: "사용자",
            UserRole.MANAGER: "관리자",
        }[self]

    # 사용법 print(UserRole.BASIC.display) -> 출력: 사용자


class UserGender(Enum):
    MALE = "male"
    FEMALE = "female"

    @property
    def display(self):
        return {
            UserGender.MALE: "남성",
            UserGender.FEMALE: "여성",
        }[self]
