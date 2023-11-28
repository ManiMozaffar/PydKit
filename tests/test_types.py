from decimal import Decimal

from pydantic import BaseModel

from pydkit.types import InSensitiveInt


def test_insensitiveint():
    class TestSchema(BaseModel):
        test: InSensitiveInt

    result = TestSchema(test=1.3)  # type: ignore
    assert result.test == int(1.3)

    result = TestSchema(test=Decimal(1.3))  # type: ignore
    assert result.test == int(Decimal(1.3))
