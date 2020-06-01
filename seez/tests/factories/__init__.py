import factory
from haps import Container

from seez.infrastructure.session import Session


class SQLAlchemyBase(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        cls._meta.sqlalchemy_session = Container().get_object(Session)

        return super()._create(model_class, *args, **kwargs)
