# PydKit

[![Release](https://img.shields.io/github/v/release/manimozaffar/pydkit)](https://img.shields.io/github/v/release/manimozaffar/pydkit)
[![Build status](https://img.shields.io/github/actions/workflow/status/manimozaffar/pydkit/main.yml?branch=main)](https://github.com/manimozaffar/pydkit/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/manimozaffar/pydkit/branch/main/graph/badge.svg)](https://codecov.io/gh/manimozaffar/pydkit)
[![Commit activity](https://img.shields.io/github/commit-activity/m/manimozaffar/pydkit)](https://img.shields.io/github/commit-activity/m/manimozaffar/pydkit)
[![License](https://img.shields.io/github/license/manimozaffar/pydkit)](https://img.shields.io/github/license/manimozaffar/pydkit)

Extended kit and tools for pydantic, to enjoy pydantic even more!

- **Github repository**: <https://github.com/manimozaffar/pydkit/>


## Contribution

I'll work on this library in few months, i don't have free time right now, but feel free to contribute.
I'll check and test the PRs myself!

## Features

Use case of CSV read/write would be:


1. Saving to a CSV file

```python
from pydkit import csv
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

users = [
    User(id=1, name="Alice"),
    User(id=2, name="Abbas"),
]
csv.save("file.csv", users)
```

2. Reading from a CSV file

```python
from pydkit.csv import read, StrNone
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    last_name: None | StrNone = None
    # StrNone helps you with reading from csv files!

users = csv.read("file.csv", User) # now user is list of User
```


3. Type extensions -> Auto converter types

```python
from pydkit.timezones import UTCTime

class User(BaseModel):
    created_at: UTCTime
```

now if you use this model, it'll convert timezones to UTC automatically in your FastAPI application
or else, you can also write custom validation

```python
from pydkit.timezones import UTCBiggerThanNow

class User(BaseModel):
    future_ts: UTCBiggerThanNow
```

