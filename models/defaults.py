from typing import Annotated
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass



pk = Annotated[int, mapped_column(index=True, primary_key=True, autoincrement=True)]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=func.now())]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]