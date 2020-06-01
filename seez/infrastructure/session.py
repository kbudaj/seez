from typing import cast

from haps import base, egg, inject, scope
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
