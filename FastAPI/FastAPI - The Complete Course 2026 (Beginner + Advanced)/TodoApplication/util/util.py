from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from database import Sessionlocal
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError

from config import ALGORITHM, SECRET_KEY

# --------------------------------------------------------------------
import logging

# configure logging once, e.g. at the top of util.py or in main.py
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# --------------------------------------------------------------------

oAuth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = Sessionlocal()

    try:
        yield db
    finally:
        db.close()


# Dependency injection (declares that get_db is needed for the function to work)
db_dependency = Annotated[Session, Depends(get_db)]


async def get_current_user(token: Annotated[str, Depends(oAuth2_bearer)]):
    try:
        logger.debug(" inside get_current_user")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        userId: int | None = payload.get("id")
        user_role: str = payload.get("role")

        if userId is None or username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Re-verify your credentials",
            )
        return {"username": username, "id": userId, "role": user_role}
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Auth token expired. Login again",
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"error: {e}",
        )


user_dependency = Annotated[dict, Depends(get_current_user)]
