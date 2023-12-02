import csv
from typing import Annotated, TypeVar, Type, Iterable

from pydantic import BaseModel, BeforeValidator

T = TypeVar("T", bound=BaseModel)

StrNone = Annotated[None, BeforeValidator(lambda v: None if v == "" else v)]
"""turn empty string to None, this is default behavior by csv built in package in python"""


# Newer implementation and design decisions to make the pydkit.csv module
# fully compatible with python standard library `csv` module
# Almost all the `csv` module APIs will be reserved + some modifications to gain Pydantic features

# Reader utilities

# csv.reader
# docs:
#   https://docs.python.org/3/library/csv.html#csv.reader
#   https://docs.python.org/3/library/csv.html#reader-objects


def reader(csvfile: Iterable[str], model: Type[T], dialect="excel", **fmtparams) -> "_Reader":
    """Return a reader object similar to Python `csv._reader`"""
    csv_reader = csv.reader(csvfile, dialect=dialect, **fmtparams)
    return _Reader(csv_reader, model)


class _Validate:
    def _validate(self, row) -> Type[T]:
        return self.model(**dict(zip(self.model.model_fields.keys(), row)))


class _Reader(_Validate):
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
        data = self._validate(raw_row)
        return list(data.model_dump().values())

    @property
    def dialect(self):
        return self.reader_object.dialect

    @property
    def line_num(self):
        return self.reader_object.line_num


# csv.DictReader
# docs:
#   https://docs.python.org/3/library/csv.html#csv.DictReader
#   https://docs.python.org/3/library/csv.html#reader-objects


class DictReader:
    def __init__(
        self,
        f,
        model: Type[T],
        fieldnames=None,
        restkey=None,
        dialect="excel",
        *args,
        **kwds,
    ):
        """Mimic the csv.DictReader object

        The fieldnames parameter is a sequence.
        If fieldnames is omitted, the values in the first row of file `f`
        will be used as the fieldnames. Regardless of how the fieldnames are determined,
        the dictionary preserves their original ordering.

        If a row has more fields than fieldnames, the remaining data is put in a list
        and stored with the fieldname specified by restkey (which defaults to None).

        Because YOU are defining the models with Pydantic,
        there is no need for `restval` parameter

        All other optional or keyword arguments are passed to the underlying reader instance.
        """
        self.dict_reader = csv.DictReader(f, fieldnames=fieldnames, restkey=restkey, dialect=dialect, *args, **kwds)
        self.model = model

    @property
    def fieldnames(self):
        return self.dict_reader.fieldnames

    def __iter__(self):
        return self

    def __next__(self):
        raw_row: dict = next(self.dict_reader)
        try:
            restkey_value = raw_row.pop("restkey", None)
        except KeyError:
            restkey_value = None

        data = self.model(**raw_row).model_dump()
        if restkey_value is not None:
            data[self.dict_reader.restkey] = restkey_value
        return data


# Writer utilities

# csv.writer
#   https://docs.python.org/3/library/csv.html#csv.writer
#   https://docs.python.org/3/library/csv.html#writer-objects


def writer(csvfile, model: Type[T], dialect="excel", **fmtparams):
    """Return a writer object similar to Python `csv._writer`"""
    csv_writer = csv.writer(csvfile, dialect=dialect, **fmtparams)
    return _Writer(csv_writer, model)


class _Writer(_Validate):
    def __init__(self, csv_writer_object, model: Type[T]):
        self.writer_object = csv_writer_object
        self.model = model

    @property
    def dialect(self):
        return self.writer_object.dialect

    @property
    def line_num(self):
        return self.writer_object.line_num

    def writerow(self, row):
        validated = self._validate(row)
        to_write = list(validated.model_dump().values())
        self.writer_object.writerow(to_write)

    def writerows(self, rows):
        validated_rows = [self._validate(row) for row in rows]
        to_write = [validated.model_dump().values() for validated in validated_rows]
        self.writer_object.writerows(to_write)


# def serialize(csv_str: str, model_type: Type[T]) -> list[T]:
#     """Serialize CSV into list of models"""
#     reader = DictReader(csv_str.splitlines())
#     result = [model_type(**row) for row in reader]
#     return result


# def deserialize(models: Sequence[BaseModel]) -> str:
#     """Deserialize pydantic model to CSV representation string"""
#     output = StringIO()
#     writer = DictWriter(output, fieldnames=models[0].model_fields.keys())
#     writer.writeheader()
#     for model in models:
#         writer.writerow(model.model_dump())
#     return output.getvalue()


# async def save_async(location: PathLike | str, models: Sequence[BaseModel]) -> None:
#     """Saves the model to the given location as csv"""
#     output = deserialize(models)
#     async with aiofiles.open(location, mode="w") as file:
#         await file.write(output)
#     return None


# async def read_async(location: PathLike | str, model_type: Type[T]) -> list[T]:
#     """Create models from to the given location as csv"""
#     async with aiofiles.open(location, mode="r", newline="") as file:
#         result = serialize(await file.read(), model_type)
#         return result


# def save(location: PathLike | str, models: Sequence[BaseModel]) -> None:
#     """Saves the model to the given location as csv"""
#     return syncify(save_async)(location=location, models=models)


# def read(location: PathLike | str, model_type: Type[T]) -> list[T]:
#     """Create models from to the given location as csv"""
#     return syncify(read_async)(location=location, model_type=model_type)
