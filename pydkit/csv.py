import csv
from csv import DictWriter
from io import StringIO
from os import PathLike
from typing import Annotated, Sequence, TypeVar, Iterator, Type, Iterable

import aiofiles
from asyncer import syncify
from pydantic import BaseModel, BeforeValidator

T = TypeVar("T", bound=BaseModel)

StrNone = Annotated[None, BeforeValidator(lambda v: None if v == "" else v)]
"""turn empty string to None, this is default behavior by csv built in package in python"""


# def serialize(csv_str: str, model_type: Type[T]) -> list[T]:
#     """Serialize CSV into list of models"""
#     reader = DictReader(csv_str.splitlines())
#     result = [model_type(**row) for row in reader]
#     return result


def deserialize(models: Sequence[BaseModel]) -> str:
    """Deserialize pydantic model to CSV representation string"""
    output = StringIO()
    writer = DictWriter(output, fieldnames=models[0].model_fields.keys())
    writer.writeheader()
    for model in models:
        writer.writerow(model.model_dump())
    return output.getvalue()


async def save_async(location: PathLike | str, models: Sequence[BaseModel]) -> None:
    """Saves the model to the given location as csv"""
    output = deserialize(models)
    async with aiofiles.open(location, mode="w") as file:
        await file.write(output)
    return None


# async def read_async(location: PathLike | str, model_type: Type[T]) -> list[T]:
#     """Create models from to the given location as csv"""
#     async with aiofiles.open(location, mode="r", newline="") as file:
#         result = serialize(await file.read(), model_type)
#         return result


def save(location: PathLike | str, models: Sequence[BaseModel]) -> None:
    """Saves the model to the given location as csv"""
    return syncify(save_async)(location=location, models=models)


# def read(location: PathLike | str, model_type: Type[T]) -> list[T]:
#     """Create models from to the given location as csv"""
#     return syncify(read_async)(location=location, model_type=model_type)

# Newer implementation and design decisions to make the pydkit.csv module
# fully compatible with python standard library `csv` module
# All the `csv` module APIs will be reserved + some modifications to gain Pydantic features

# Reader utilities

# csv.reader
# docs:
#   https://docs.python.org/3/library/csv.html#csv.reader
#   https://docs.python.org/3/library/csv.html#reader-objects


def reader(csvfile: Iterable[str], model: Type[T], dialect="excel", **fmtparams) -> "_Reader":
    """Return a reader object similar to Python `csv._reader`"""
    csv_reader = csv.reader(csvfile, dialect=dialect, **fmtparams)
    return _Reader(csv_reader, model)


class _Reader:
    """Mimic the csv._reader object attributes and behaviour"""

    def __init__(self, csv_reader_object, model: Type[T]):
        self.reader_object = csv_reader_object
        self.model = model
        self._header_shown = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self._header_shown:
            self._header_shown = True
            return next(self.reader_object)  # header -- doesn't need validation

        # next raw row
        raw_row = next(self.reader_object)
        return self._model_to_list_reader(raw_row)

    def _model_to_list_reader(self, raw_row) -> list:
        """Parse and Validate each row and Return the list of data

        Because the return value of Python `csv.reader` is list,
        and keeping the API as is, we should return also a list.

        The difference between `csv.reader` and `pydkit.csv.reader` is that
        the data is parsed and validated with Pydantic and the returning list items,
        have the expected types.
        """
        data = self.model(**dict(zip(self.model.model_fields.keys(), raw_row)))
        return list(data.model_dump().values())

    @property
    def dialect(self):
        return self.reader_object.dialect

    @property
    def line_num(self):
        return self.reader_object.line_num
