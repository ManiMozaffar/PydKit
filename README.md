# PydKit

[![Release](https://img.shields.io/github/v/release/manimozaffar/pydkit)](https://img.shields.io/github/v/release/manimozaffar/pydkit)
[![Build status](https://img.shields.io/github/actions/workflow/status/manimozaffar/pydkit/main.yml?branch=main)](https://github.com/manimozaffar/pydkit/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/manimozaffar/pydkit/branch/main/graph/badge.svg)](https://codecov.io/gh/manimozaffar/pydkit)
[![Commit activity](https://img.shields.io/github/commit-activity/m/manimozaffar/pydkit)](https://img.shields.io/github/commit-activity/m/manimozaffar/pydkit)
[![License](https://img.shields.io/github/license/manimozaffar/pydkit)](https://img.shields.io/github/license/manimozaffar/pydkit)

Extended kit and tools for pydantic, to enjoy pydantic even more!

- **Github repository**: <https://github.com/manimozaffar/pydkit/>


## Contribution

I'll work on this library in few months, I don't have free time right now, but feel free to contribute.
I'll check and test the PRs myself!

## Features

Similar functions and class of Python standard library `csv` module, but powered with Pydantic


### Saving to a CSV file

- Use of Pydantic models
```python
from pydkit.csv import writer
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str

    
users = [
    User(id=1, name="Alice"),
    User(id=2, name="Abbas"),
]

with open('users.csv', 'w') as f:
    kit_writer = writer(f, model=User)
    kit_writer.writerow(User.model_fields, header=True)
    kit_writer.writerows(users)
```
results in:
```csv
id,name
1,Alice
2,Abbas
```

- Validation before writing
```python
from pydkit.csv import writer
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


users = [[1, "Mahdi"], [2.3, "Zohre"]]

with open("users.csv", "w") as f:
    kit_writer = writer(f, model=User)
    kit_writer.writerow(User.model_fields, header=True)
    kit_writer.writerows(users)
```
results in:
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for User
id
  Input should be a valid integer, got a number with a fractional part [type=int_from_float, input_value=2.3, input_type=float]
    For further information visit https://errors.pydantic.dev/2.5/v/int_from_float
```


### Reading from a CSV file

```
id,name,age,gender
1,Mahdi,21,male
2,Zohre,21,female
3,Alice,34
```

```python
from typing import Literal

from pydkit.csv import reader, StrNone
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    age: int
    gender: Literal["male", "female", "others"] | StrNone = None


with open('users.csv') as f:
    kit_reader = reader(f, model=User)
    for row in kit_reader:
        print(row)
```
results in:
```
['id', 'name', 'age', 'gender']
[1, 'Mahdi', 21, 'male']
[2, 'Zohre', 21, 'female']
[3, 'Alice', 34, None]
```
notice the type conversion.

- Validation
```
id,name,age,gender
1,Mahdi,21.5,male
```

```python
from typing import Literal

from pydkit.csv import reader, StrNone
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    age: int
    gender: Literal["male", "female", "others"] | StrNone = None


with open('users.csv') as f:
    kit_reader = reader(f, model=User)
    for row in kit_reader:
        print(row)
```
results in:
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for User
age
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='21.5', input_type=str]
    For further information visit https://errors.pydantic.dev/2.5/v/int_parsing
```

### Type extensions -> Auto converter types

```python
from pydkit.timezones import UTCTime
from pydantic import BaseModel


class User(BaseModel):
    created_at: UTCTime
```

now if you use this model, it'll convert timezones to UTC automatically in your FastAPI application
or else, you can also write custom validation

```python
from pydkit.timezones import UTCBiggerThanNow
from pydantic import BaseModel


class User(BaseModel):
    future_ts: UTCBiggerThanNow
```

