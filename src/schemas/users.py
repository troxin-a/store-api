import re
from typing_extensions import Self
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, model_validator


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        pattern = r"^\+7\d{10}$"
        if not re.match(pattern, v):
            raise ValueError("Телефон должен начинаться с +7 и содержать 10 цифр.")
        return v


class CreateUser(UserBase):
    password1: str
    password2: str

    @field_validator("password1")
    @classmethod
    def validate_password(cls, v):
        pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[$%&!:])(?=.{8,})[A-Za-z\d$%&!:]*$"
        if not re.match(pattern, v):
            raise ValueError(
                "Пароль должен быть не менее 8 символов, только латиница, минимум 1 цифра, минимум 1 символ верхнего регистра, минимум 1 спец символ ($%&!:)."
            )
        return v

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        pw1 = self.password1
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("Пароли не совпадают.")
        return self


class UserRead(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ListUser(UserBase):
    id: int
    is_active: bool
    is_admin: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
