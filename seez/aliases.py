from typing import NewType
from uuid import UUID

CarPk = NewType("CarPk", UUID)
Year = NewType("Year", int)
Mileage = NewType("Mileage", int)
Price = NewType("Price", int)
Color = NewType("Color", str)

MakePk = NewType("MakePk", UUID)
MakeName = NewType("MakeName", str)

ModelPk = NewType("ModelPk", UUID)
ModelName = NewType("ModelName", str)

SubModelPk = NewType("SubModelPk", UUID)
SubModelName = NewType("SubModelName", str)
