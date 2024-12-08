from api.v1.endpoints import shifts
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi_users import exceptions, schemas
from fastapi_users.router import ErrorCode
from fastapi_users.router.common import ErrorModel
from fastapi_users.router.reset import RESET_PASSWORD_RESPONSES

from src.schemas.users import UserCreate, UserRead, UserUpdate
from src.users import UserManager, auth_backend, fastapi_users, get_user_manager


def custom_reset_password_router():
    """ Redefined router for reset password. """
    router = APIRouter()

    @router.post(
        "/forgot-password",
        status_code=status.HTTP_202_ACCEPTED,
        name="reset:forgot_password",
    )
    async def forgot_password(
            request: Request,
            username: str = Body(..., embed=True),
            user_manager: UserManager = Depends(get_user_manager),
    ):
        try:
            user = await user_manager.get_by_email(username)
        except exceptions.UserNotExists:
            return

        try:  # noqa: SIM105
            await user_manager.forgot_password(user, request)
        except exceptions.UserInactive:
            pass

        return

    @router.post(
        "/reset-password",
        name="reset:reset_password",
        responses=RESET_PASSWORD_RESPONSES,
    )
    async def reset_password(
            request: Request,
            token: str = Body(...),
            password: str = Body(...),
            user_manager: UserManager = Depends(get_user_manager),
    ):
        try:
            await user_manager.reset_password(token, password, request)
        except (
                exceptions.InvalidResetPasswordToken,
                exceptions.UserNotExists,
                exceptions.UserInactive,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
            ) from None
        except exceptions.InvalidPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                    "reason": e.reason,
                },
            ) from e

    return router


def custom_verify_router():
    """ Redefined router for verify user. """
    router = APIRouter()

    @router.post(
        "/request-verify-token",
        status_code=status.HTTP_202_ACCEPTED,
        name="verify:request-token",
    )
    async def request_verify_token(
            request: Request,
            username: str = Body(..., embed=True),
            user_manager: UserManager = Depends(get_user_manager),
    ):
        try:
            user = await user_manager.get_by_email(username)
            await user_manager.request_verify(user, request)
        except (
                exceptions.UserNotExists,
                exceptions.UserInactive,
                exceptions.UserAlreadyVerified,
        ):
            pass


    @router.post(
        "/verify",
        response_model=UserRead,
        name="verify:verify",
        responses={
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorCode.VERIFY_USER_BAD_TOKEN: {
                                "summary": "Bad token, not existing user or"
                                           "not the username currently set for the user.",
                                "value": {"detail": ErrorCode.VERIFY_USER_BAD_TOKEN},
                            },
                            ErrorCode.VERIFY_USER_ALREADY_VERIFIED: {
                                "summary": "The user is already verified.",
                                "value": {
                                    "detail": ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
                                },
                            },
                        },
                    },
                },
            },
        },
    )
    async def verify(
            request: Request,
            token: str = Body(..., embed=True),
            user_manager: UserManager = Depends(get_user_manager),
    ):
        try:
            user = await user_manager.verify(token, request)
            return schemas.model_validate(UserRead, user)
        except (exceptions.InvalidVerifyToken, exceptions.UserNotExists):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
            ) from None
        except exceptions.UserAlreadyVerified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
            ) from None

    return router


api_router = APIRouter()

api_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=['auth'],
)
api_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)
api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
api_router.include_router(
    custom_reset_password_router(),
    prefix='/auth',
    tags=['auth'],
)
api_router.include_router(
    custom_verify_router(),
    prefix='/auth',
    tags=['auth'],
)
api_router.include_router(
    shifts.router,
    prefix='/shifts',
    tags=['shifts'],
)
