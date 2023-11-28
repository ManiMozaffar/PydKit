from datetime import UTC, datetime, timezone
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class UTCTime(datetime):
    strict: bool = True
    """Will raise value error if timezone info is missing"""

    _tz = UTC
    """Timezone for the class implementation"""

    @classmethod
    def _perform_validation(cls, value: datetime, strict: bool = True):
        """Override this method to perform validation on the given value"""
        if value.tzinfo is None:
            if strict:
                raise ValueError("Timezone Info should be passed")
            # Assume it's in UTC in non-strict mode
            return value.astimezone(timezone.utc)

        if value.tzinfo != timezone.utc:
            return value.astimezone(timezone.utc)
        return value

    def __new__(cls, value: datetime, *args, **kwargs):
        if isinstance(value, datetime):
            value = cls._perform_validation(value, cls.strict)
            return super().__new__(
                cls,
                value.year,
                value.month,
                value.day,
                value.hour,
                value.minute,
                value.second,
                value.microsecond,
                cls._tz,
            )

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(datetime))


class UTCBiggerThanNow(UTCTime):
    @classmethod
    def _perform_validation(cls, value: datetime, strict: bool = True):
        value = UTCTime._perform_validation(value, strict)
        if value < datetime.now(timezone.utc):
            raise ValueError("UTC Datetime should be bigger than now")

        return value
