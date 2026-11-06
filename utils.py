from argon2 import PasswordHasher
from select import select
from models.user import User

from dependencies import AccessTokenDep, DB_DEP
ph = PasswordHasher()


def hash_password(password):
    return ph.hash(password)

def verify_password(hashed_password, user_password):
    return ph.verify(hashed_password, user_password)


async def check_admin(payload: AccessTokenDep, session: DB_DEP ) -> bool:
    pk = int(payload.sub)
    stmt = select(User).where(User.pk == pk)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        return False

    else:
        if user.admin:
            return True
        else:
            return False



