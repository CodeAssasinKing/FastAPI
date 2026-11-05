from typing import Annotated

from authx import TokenPayload
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.jwt import security
from database_connection import get_session

DB_DEP = Annotated[AsyncSession, Depends(get_session)]

AccessTokenDep = Annotated[TokenPayload, Depends(security.access_token_required)]
RefreshTokenDep = Annotated[TokenPayload, Depends(security.refresh_token_required)]