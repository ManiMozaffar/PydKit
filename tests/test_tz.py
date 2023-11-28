from datetime import datetime, timedelta, timezone

import pytest
from pydantic import BaseModel

from pydkit.timezones import UTCBiggerThanNow, UTCTime


class ExampleModel(BaseModel):
    created_at: UTCTime


def test_utctime_with_naive_datetime():
    naive_datetime = datetime(2023, 1, 1, 12, 0, 0)
    with pytest.raises(ValueError):
        UTCTime(naive_datetime)


def test_utctime_with_utc_datetime():
    utc_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    utctime = UTCTime(utc_datetime)
    assert utctime.tzinfo is timezone.utc


def test_utctime_with_non_utc_datetime():
    non_utc_datetime = datetime(
        2023, 1, 1, 12, 0, 0, tzinfo=timezone(timedelta(hours=2))
    )
    utctime = UTCTime(non_utc_datetime)
    assert utctime.tzinfo is timezone.utc
    result = ExampleModel(created_at=non_utc_datetime)  # type: ignore
    assert result.created_at.tzinfo == utctime.tzinfo
    assert str(result.created_at) == str(utctime)
    assert str(result.created_at) != str(non_utc_datetime)


def test_utctime_is_instance_of_datetime():
    utc_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    utctime = UTCTime(utc_datetime)
    assert isinstance(utctime, datetime)


def test_utc_bigger_than_now_with_past_datetime():
    past_datetime = datetime.now(timezone.utc) - timedelta(days=1)
    with pytest.raises(ValueError):
        UTCBiggerThanNow(past_datetime)


def test_utc_bigger_than_now_with_future_datetime():
    future_datetime = datetime.now(timezone.utc) + timedelta(days=1)
    utc_bigger_than_now = UTCBiggerThanNow(future_datetime)
    assert utc_bigger_than_now > datetime.now(timezone.utc)
