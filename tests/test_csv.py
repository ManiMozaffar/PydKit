from typing import Literal

import pytest
from pydantic import BaseModel

from pydkit.csv import StrNone, read_async, save_async


class User(BaseModel):
    id: int
    name: str
    gender: Literal["male", "female", "others"] | StrNone = None
    age: int


@pytest.mark.asyncio
async def test_csv():
    users = [
        User(id=1, name="Alice", age=30, gender=None),
        User(id=2, name="Abbas", age=30),
    ]
    await save_async("logs/user.csv", users)
    loaded_users = await read_async("logs/user.csv", User)
    for idx, user in enumerate(users):
        for field in user.model_fields.keys():
            assert getattr(user, field) == getattr(loaded_users[idx], field)
