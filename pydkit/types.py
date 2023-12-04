from decimal import Decimal
from typing import Annotated

from pydantic import BeforeValidator

InsensitiveInt = Annotated[
    int,
    BeforeValidator(lambda v: int(v) if isinstance(v, (float, Decimal)) else v),
]
