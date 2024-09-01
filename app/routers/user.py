from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import get_user_service
from auth import create_access_token, verify_password
from schemas import UserOutSchema, UserCreateSchema, UserTokenSchema, UserResetPasswordResponseSchema, UserResetPasswordSchema
from services import UserService

router = APIRouter(tags=['users'])

@router.post('/register', response_model=UserOutSchema)
def register(user: UserCreateSchema, user_service: UserService = Depends(get_user_service)):
    db_user = user_service.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')
    new_user = user_service.create_user(user)
    return UserOutSchema.model_validate(new_user)

@router.post('/login', response_model=UserTokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends(get_user_service)):
    ## OAuth2PasswordRequestFormはusernameを使用する
    db_user = user_service.get_user_by_email(email=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={'sub': db_user.email})
    return UserTokenSchema(access_token=access_token, token_type="bearer")

@router.post('/reset-password', response_model=UserResetPasswordResponseSchema)
def reset_password(request: UserResetPasswordSchema, user_service: UserService = Depends(get_user_service)):
    if user_service.reset_password(request.new_password):
        return UserResetPasswordResponseSchema(message='Password successfully updated.')
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Password update failed.'
    )
