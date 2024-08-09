from pydantic import BaseModel, ConfigDict, EmailStr

class UserSchema(BaseModel):
    id: int
    email: str

class UserOutSchema(UserSchema):
    model_config = ConfigDict(from_attributes=True)

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str

class UserTokenSchema(BaseModel):
    access_token: str
    token_type: str

class UserResetPasswordResponseSchema(BaseModel):
    message: str

class UserResetPasswordSchema(BaseModel):
    token: str
    new_password: str