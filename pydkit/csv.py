from csv import DictReader, DictWriter
from io import StringIO
from os import PathLike
from typing import Annotated, Sequence, Type, TypeVar

import aiofiles
from asyncer import syncify
from pydantic import BaseModel, BeforeValidator

T = TypeVar("T", bound=BaseModel)

StrNone = Annotated[None, BeforeValidator(lambda v: None if v == "" else v)]
"""turn empty string to None, this is default behavior by csv built in package in python"""


def serialize(csv_str: str, model_type: Type[T]) -> list[T]:
    """Serialize CSV into list of models"""
    reader = DictReader(csv_str.splitlines())
    result = [model_type(**row) for row in reader]
    return result


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


async def read_async(location: PathLike | str, model_type: Type[T]) -> list[T]:
    """Create models from to the given location as csv"""
    async with aiofiles.open(location, mode="r", newline="") as file:
        result = serialize(await file.read(), model_type)
        return result


def save(location: PathLike | str, models: Sequence[BaseModel]) -> None:
    """Saves the model to the given location as csv"""
    return syncify(save_async)(location=location, models=models)


def read(location: PathLike | str, model_type: Type[T]) -> list[T]:
    """Create models from to the given location as csv"""
    return syncify(read_async)(location=location, model_type=model_type)
