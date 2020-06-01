from typing import NewType, TypeVar
from uuid import UUID

CarPk = NewType("CarPk", UUID)
T = TypeVar("T")
TEntity = TypeVar("TEntity")
