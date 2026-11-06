from fastapi import APIRouter, status, HTTPException, Response
from sqlalchemy import select

from config.jwt import security
from dependencies import DB_DEP, AccessTokenDep, RefreshTokenDep
from schemas.users import UserCreate, UserGet, UserUpdate
from models.user import User
from utils import hash_password, verify_password, check_admin
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate


router = APIRouter(
    prefix="/auth",
)


@router.post("/sign-up", summary="Sign Up to platform")
async def sign_up(
        session : DB_DEP,
        user: UserCreate,
):
    stmt = select(User).where(User.username == user.username)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()

    if found_user:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")


    hashed_password = hash_password(user.password)

    try:
        new_user = User(
            password=hashed_password,
            username=user.username
        )

        session.add(new_user)

        await session.commit()

        await session.refresh(new_user)

        return UserGet.model_validate(new_user)

    except Exception as e:
        print(e)
        await session.rollback()
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot create new user")




@router.post("/login", summary="Login to platform")
async def login(
        session : DB_DEP,
        user: UserCreate,
        response: Response
):
    stmt = select(User).where(User.username == user.username)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()

    if not found_user:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")


    if found_user and verify_password(found_user.password, user.password):
        access_token = security.create_access_token(uid=str(found_user.pk))
        refresh_token = security.create_refresh_token(uid=str(found_user.pk))
        security.set_access_cookies(
            access_token, response)
        security.set_refresh_cookies(
            refresh_token, response
        )
        return HTTPException(status_code=status.HTTP_200_OK, detail="Login successful")
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")






@router.post("/logout", summary="Logout from platform")
async def logout(
        response : Response,
):
    security.unset_access_cookies(response)
    security.unset_refresh_cookies(response)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Logout successful")



@router.post("/refresh", summary="Refresh token")
async def refresh(
        payload: RefreshTokenDep,
        response: Response,
):
    access_token = security.create_access_token(uid=str(payload.sub))
    refresh_token = security.create_refresh_token(uid=str(payload.sub))
    security.set_access_cookies(
        access_token, response)
    security.set_refresh_cookies(
        refresh_token, response
    )
    return HTTPException(status_code=status.HTTP_200_OK, detail="Refresh is successful")



@router.get("/me", summary="Return user info")
async def me(
        session : DB_DEP,
        payload: AccessTokenDep
):
    stmt = select(User).where(User.pk == int(payload.sub))
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()

    if found_user:
        return UserGet.model_validate(found_user)
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)



@router.delete("/delete", summary="Delete self account")
async def delete_user(
        session : DB_DEP,
        payload: AccessTokenDep,
):
    stmt = select(User).where(User.pk == int(payload.sub))
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()

    if found_user:
        await session.delete(found_user)
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)



@router.delete("/soft-delete/{user_pk}", summary="Ban user account")
async def soft_delete_user(
        session : DB_DEP,
        payload: AccessTokenDep,
        user_pk: int,
):
    is_admin = await check_admin(payload, session)
    if not is_admin:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    stmt = select(User).where(User.pk == user_pk)
    result = await session.execute(stmt)
    user_to_ban = result.scalar_one_or_none()

    if not user_to_ban:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # ban function
    user_to_ban.banned = True
    session.add(user_to_ban)
    await session.commit()
    await session.refresh(user_to_ban)
    return UserGet.model_validate(user_to_ban)




@router.get("/all_users", summary="Return all users", response_model=Page[UserGet])
async def get_all_users(session: DB_DEP, payload: AccessTokenDep):
    is_admin = await check_admin(payload, session)
    if not is_admin:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    stmt = select(User).order_by(User.pk)
    return await apaginate(session, stmt)




@router.patch("/update-me", summary="Update user info")
async def update_me(
        session: DB_DEP,
        payload: AccessTokenDep,
        user_data: UserUpdate
):
    stmt = select(User).where(User.pk == int(payload.sub))
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()

    if not found_user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if user_data.username:
        found_user.username = user_data.username

    if user_data.password:
        found_user.password = hash_password(user_data.password)

    session.add(found_user)
    await session.commit()
    return UserGet.model_validate(found_user)