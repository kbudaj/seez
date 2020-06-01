from functools import wraps
from typing import Any, cast

from haps import Container, base, egg, inject, scope
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session as SqlSession
from sqlalchemy.orm import sessionmaker as SqlSessionMaker

from seez import settings
from seez.infrastructure.scopes import THREAD_SCOPE, TRANSACTIONAL_SCOPE


@base
class Session(SqlSession):
    pass


@base
class SessionMaker(SqlSessionMaker):
    pass


@egg
@scope(THREAD_SCOPE)
def sql_alchemy_session_maker() -> SessionMaker:
    engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
    session_maker = SqlSessionMaker(expire_on_commit=False, bind=engine)

    return cast(SessionMaker, session_maker)


@egg
@scope(TRANSACTIONAL_SCOPE)
@inject
def sql_alchemy_session_factory(session_maker: SessionMaker) -> Session:
    return cast(Session, session_maker())


def transactional(func: Any) -> Any:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        transactional_scope = Container().scopes[TRANSACTIONAL_SCOPE]  # noqa

        with transactional_scope.scope:
            session = Container().get_object(Session)

            try:
                ret = func(*args, **kwargs)
                session.commit()
                session.close()
            except Exception:
                session.close()
                raise
            else:
                return ret

    return wrapper
