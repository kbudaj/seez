from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper, relationship

from seez.domain.models import Car, Make, Model, SubModel
from seez.infrastructure.postgres import METADATA

CAR_TABLE = Table(
    "car",
    METADATA,
    Column("pk", UUID(as_uuid=True), primary_key=True),
    Column("active", Boolean, nullable=False, default=True, index=True),
    Column("year", Integer, nullable=False),
    Column("mileage", Integer, nullable=True),
    Column("price", Integer, nullable=True),
    Column("exterior_color", Text, nullable=True),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow),
    Column("updated_at", DateTime, nullable=False, default=datetime.utcnow),
    Column(
        "submodel_pk",
        UUID(as_uuid=True),
        ForeignKey("submodel.pk"),
        index=True,
        nullable=False,
    ),
    Column("body_type", Enum(Car.BodyType), key="_body_type", nullable=True),
    Column("transmission", Enum(Car.Transmission), key="_transmission", nullable=True),
    Column("fuel_type", Enum(Car.FuelType), key="_fuel_type", nullable=True),
)

MAKE_TABLE = Table(
    "make",
    METADATA,
    Column("pk", UUID(as_uuid=True), primary_key=True),
    Column("name", Text, nullable=False, unique=True),
    Column("active", Boolean, nullable=False, default=True, index=True),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow),
    Column("updated_at", DateTime, nullable=False, default=datetime.utcnow),
)

MODEL_TABLE = Table(
    "model",
    METADATA,
    Column("pk", UUID(as_uuid=True), primary_key=True),
    Column("name", Text, nullable=False),
    Column("active", Boolean, nullable=False, default=True, index=True),
    Column(
        "make_pk", UUID(as_uuid=True), ForeignKey("make.pk"), nullable=False, index=True
    ),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow),
    Column("updated_at", DateTime, nullable=False, default=datetime.utcnow),
)

SUBMODEL_TABLE = Table(
    "submodel",
    METADATA,
    Column("pk", UUID(as_uuid=True), primary_key=True),
    Column("name", Text, nullable=True),
    Column("active", Boolean, nullable=False, default=True),
    Column(
        "model_pk", UUID(as_uuid=True), ForeignKey("model.pk"), nullable=False, index=True
    ),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow),
    Column("updated_at", DateTime, nullable=False, default=datetime.utcnow),
)

mapper(Car, CAR_TABLE, properties={"_submodel": relationship(SubModel)})
mapper(Make, MAKE_TABLE)
mapper(Model, MODEL_TABLE, properties={"_make": relationship(Make)})
mapper(SubModel, SUBMODEL_TABLE, properties={"_model": relationship(Model)})
