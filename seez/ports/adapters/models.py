from sqlalchemy import Column, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper

from seez.ports.adapters.postgres import METADATA

from seez.domain.models import Car

CAR_TABLE = Table(
    "car",
    METADATA,
    Column("pk", UUID(as_uuid=True), primary_key=True),
    Column("title", Text, nullable=False),
)

mapper(Car, CAR_TABLE)
