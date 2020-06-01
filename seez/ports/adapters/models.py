import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper

from seez.domain.models import Car
from seez.infrastructure.postgres import METADATA

CAR_TABLE = Table(
    "car",
    METADATA,
    Column("pk", UUID(as_uuid=True), primary_key=True),
    Column("active", Boolean, nullable=False, default=True, index=True),
    Column("year", Integer),
    Column("mileage", Integer),
    Column("price", Integer),
    Column("exterior_color", Text),
    Column("created_at", DateTime, nullable=False, dafault=datetime.utcnow),
    Column("updated_at", DateTime, nullable=True),
    Column("make_pk", UUID(as_uuid=True), ForeignKey("make.pk"), index=True),
    Column("model_pk", UUID(as_uuid=True), ForeignKey("model.pk"), index=True),
    Column("submodel_pk", UUID(as_uuid=True), ForeignKey("submodel.pk"), index=True),
    Column("body_type", Enum(Car.BodyType), key="_body_type"),
    Column("transmission", Enum(Car.Transmission), key="_transmission"),
    Column("fuel_type", Enum(Car.FualType), key="_fuel_type"),
)

mapper(Car, CAR_TABLE)
