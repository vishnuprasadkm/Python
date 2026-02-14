from util.util import get_current_user, SECRET_KEY, ALGORITHM
from jose import jwt
import pytest

from fastapi import HTTPException, status


@pytest.mark.asyncio
async def test_get_current_user():
    encode = {"sub": "user", "id": 5, "role": "user"}
    token = jwt.encode(encode, SECRET_KEY, ALGORITHM)

    user = await get_current_user(token)
    assert user == {"username": "user", "id": 5, "role": "user"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"id": 5, "role": "user"}
    token = jwt.encode(encode, SECRET_KEY, ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Re-verify your credentials"

