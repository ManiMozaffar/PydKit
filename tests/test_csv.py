import csv
from typing import Literal
from tempfile import NamedTemporaryFile

import pytest
from pydantic import BaseModel, ValidationError

from pydkit.csv import StrNone, reader, DictReader, writer


class User(BaseModel):
    id: int
    name: str
    age: int
    gender: Literal["male", "female", "others"] | StrNone = None


@pytest.mark.parametrize(
    ["to_write", "expected"],
    [
        (["1", "Zohre", "30", "female"], [1, "Zohre", 30, "female"]),
        (["2", "Mahdi", 25, "male"], [2, "Mahdi", 25, "male"]),
        (["3", "Alice", "25.0", None], [3, "Alice", 25, None]),
        (["4", "John", 33.0, ""], [4, "John", 33, None]),
        (["5", "Mary", "36"], [5, "Mary", 36, None]),
    ],
)
def test_reader(to_write, expected):
    """Test pydkit.csv.reader"""
    with NamedTemporaryFile(mode="w", delete=False) as tf:
        writer_ = csv.writer(tf)
        writer_.writerow(["id", "name", "age", "gender"])
        writer_.writerow(to_write)
        tf.close()

        with open(tf.name) as csvfile:
            kit_reader = reader(csvfile, model=User)
            next(kit_reader)  # header
            assert expected == next(kit_reader)


@pytest.mark.parametrize(
    ["to_write", "expected"],
    [
        ([1, "Zohre", 30, "female"], {"id": 1, "name": "Zohre", "age": 30, "gender": "female"}),
        ([2, "Mahdi", 25, "male"], {"id": 2, "name": "Mahdi", "age": 25, "gender": "male"}),
        ([3, "Alice", 25, None], {"id": 3, "name": "Alice", "age": 25, "gender": None}),
        ([4, "John", 33, ""], {"id": 4, "name": "John", "age": 33, "gender": None}),
        ([5, "Mary", 36], {"id": 5, "name": "Mary", "age": 36, "gender": None}),
    ],
)
def test_dict_reader(to_write, expected):
    """Test pydkit.DictReader"""
    with NamedTemporaryFile(mode="w", delete=False) as tf:
        writer_ = csv.writer(tf)
        writer_.writerow(["id", "name", "age", "gender"])
        writer_.writerow(to_write)
        tf.close()

        with open(tf.name) as csvfile:
            dict_reader = DictReader(csvfile, User)
            assert expected == next(dict_reader)


def test_writer_writerow_model():
    """Test pydkit.writer.writerow"""
    with NamedTemporaryFile(mode="w", delete=False) as tf:
        header = ["id", "name", "age", "gender"]
        kit_writer = writer(tf, User)
        kit_writer.writerow(header, header=True)

        user = User(id=1, name="Alice", age=30, gender="female")
        kit_writer.writerow(user)

        tf.close()

        with open(tf.name) as csvfile:
            kit_reader = reader(csvfile, User)
            next(kit_reader)  # header
            assert [1, "Alice", 30, "female"] == next(kit_reader)


def test_writer_writerow_raw_row():
    """Test pydkit.writer.writerow"""
    with NamedTemporaryFile(mode="w", delete=False) as tf:
        header = ["id", "name", "age", "gender"]
        kit_writer = writer(tf, User)
        kit_writer.writerow(header, header=True)

        user = [1, "Alice", 30, "female"]
        kit_writer.writerow(user)

        tf.close()

        with open(tf.name) as csvfile:
            kit_reader = reader(csvfile, User)
            next(kit_reader)  # header
            assert [1, "Alice", 30, "female"] == next(kit_reader)


def test_writer_writerow_raw_row_incorrect_data():
    with NamedTemporaryFile(mode="w", delete=False) as tf:
        header = ["id", "name", "age", "gender"]
        kit_writer = writer(tf, User)
        kit_writer.writerow(header, header=True)

        user = [1, "Alice", 30, "femail"]
        with pytest.raises(ValidationError):
            kit_writer.writerow(user)


def test_writer_writerows_model():
    """Test pydkit.writer.writerows"""
    with NamedTemporaryFile(mode="w", delete=False) as tf:
        header = ["id", "name", "age", "gender"]
        kit_writer = writer(tf, User)
        kit_writer.writerow(header, header=True)

        users = [
            User(id=1, name="Alice", age=30, gender="female"),
            User(id=2, name="Mahdi", age=21, gender="male"),
        ]
        kit_writer.writerows(users)

        tf.close()

        with open(tf.name) as csvfile:
            kit_reader = reader(csvfile, User)
            next(kit_reader)  # header
            assert [1, "Alice", 30, "female"] == next(kit_reader)
            assert [2, "Mahdi", 21, "male"] == next(kit_reader)


def test_writer_writerows_raw_row():
    """Test pydkit.writer.writerows"""
    with NamedTemporaryFile(mode="w", delete=False) as tf:
        header = ["id", "name", "age", "gender"]
        kit_writer = writer(tf, User)
        kit_writer.writerow(header, header=True)

        users = [
            [1, "Alice", 30, "female"],
            [2, "Mahdi", 21, "male"],
        ]
        kit_writer.writerows(users)

        tf.close()

        with open(tf.name) as csvfile:
            kit_reader = reader(csvfile, User)
            next(kit_reader)  # header
            assert [1, "Alice", 30, "female"] == next(kit_reader)
            assert [2, "Mahdi", 21, "male"] == next(kit_reader)


def test_writer_writerows_raw_row_incorrect_data():
    with NamedTemporaryFile(mode="w", delete=False) as tf:
        header = ["id", "name", "age", "gender"]
        kit_writer = writer(tf, User)
        kit_writer.writerow(header, header=True)

        users = [
            [1, "Alice", 30, "female"],
            [2, "Mahdi", 21, "mail"],
        ]
        with pytest.raises(ValidationError):
            kit_writer.writerows(users)
