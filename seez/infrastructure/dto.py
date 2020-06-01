from abc import abstractmethod

from pydantic import BaseModel

from seez.infrastructure.models import Entity


class DTO(BaseModel):
    @abstractmethod
    def from_model(cls, model: Entity) -> "DTO":
        pass
