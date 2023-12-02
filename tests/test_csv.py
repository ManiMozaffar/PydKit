import csv
from typing import Literal
from tempfile import NamedTemporaryFile

import pytest
from pydantic import BaseModel

from pydkit.csv import StrNone, reader


class User(BaseModel):
    id: int
    name: str
    age: int
    gender: Literal["male", "female", "others"] | StrNone = None


@pytest.mark.parametrize(
    ['to_write', 'expected'],
    [
        ([1, "Zohre", 30, "female"], [1, "Zohre", 30, "female"]),
        ([2, "Mahdi", 25, "male"], [2, "Mahdi", 25, "male"]),
        ([3, "Alice", 25, None], [3, "Alice", 25, None]),
        ([4, "John", 33, ""], [4, "John", 33, None]),
        ([5, "Mary", 36], [5, "Mary", 36, None]),
    ]
)
def test_correct_data_reader(to_write, expected):
    """Test pydkit.csv.reader with a temporary file"""
    with NamedTemporaryFile(mode="w", delete=False) as tf:
        writer = csv.writer(tf)
        writer.writerow(["id", "name", "age", "gender"])
        writer.writerow(to_write)
        tf.close()

        with open(tf.name) as csvfile:
            kit_reader = reader(csvfile, model=User)
            next(kit_reader)  # header
            assert expected == next(kit_reader)


# @pytest.mark.asyncio
# async def test_csv():
#     users = [
#         User(id=1, name="Alice", age=30, gender=None),
#         User(id=2, name="Abbas", age=30),
#     ]
#     await save_async("logs/user.csv", users)
#     loaded_users = await read_async("logs/user.csv", User)
#     for idx, user in enumerate(users):
#         for field in user.model_fields.keys():
#             assert getattr(user, field) == getattr(loaded_users[idx], field)
