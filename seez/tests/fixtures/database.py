from typing import Any, cast

import pytest
from alembic import command as alembic_command
from alembic import config as alembic_config
from haps import Container, Egg, egg, scope
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker

from seez import settings
from seez.infrastructure.postgres import METADATA
from seez.infrastructure.scopes import TRANSACTIONAL_SCOPE
from seez.infrastructure.session import Session

BASE_DB_URL, _DB = settings.DATABASE_URL.rsplit("/", maxsplit=1)
TEST_DB = "test_db"
TEST_DB_URL = f"{BASE_DB_URL}/{TEST_DB}"


class Singleton:
    """
    GLOBAL used to share transaction-scoped session between test
    and factories in that test.
    """

    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class CommonSessionMaker(Singleton):
    common_session_maker = None


@pytest.fixture(scope="session")
def setup_test_db() -> None:
    """
    Recreate a clean DB between test sessions.
    """
    engine = create_engine(BASE_DB_URL)
    connection = engine.connect()
    connection.execution_options(autocommit=False)
    connection.execute("ROLLBACK")
    try:
        connection.execute(f"DROP DATABASE {TEST_DB}")
    except ProgrammingError:
        pass  # probably doesn't exist
    finally:
        connection.execute("ROLLBACK")

    try:
        connection.execute(f"CREATE DATABASE {TEST_DB}")
    finally:
        connection.execute("ROLLBACK")

    connection.close()
    engine.dispose()


@pytest.fixture(scope="session")
def run_migrations() -> None:
    """
    Update DB schema according to migration files.
    """
    config = alembic_config.Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", TEST_DB_URL)
    config.set_main_option("script_location", "infrastructure/postgres/migrations")

    alembic_command.upgrade(config, "head")


@pytest.fixture(scope="session")
def recreate_db_from_metadata() -> None:
    """
    Update DB schema according to current models metadata.
    """
    engine = create_engine(TEST_DB_URL)
    METADATA.create_all(engine)


@pytest.fixture(scope="session")
def postgres_db(request: Any, setup_test_db: Any) -> None:
    """
    Create Test DB with updated schema based on param passed to tests.
    """
    if request.config.getvalue("run_migrations"):
        request.getfixturevalue("run_migrations")
    else:
        request.getfixturevalue("recreate_db_from_metadata")


@pytest.fixture(scope="session")
def postgres_connection(postgres_db):
    engine = create_engine(TEST_DB_URL)
    METADATA.create_all(engine)
    connection = engine.connect()

    yield connection

    connection.close()
    engine.dispose()


@pytest.fixture
def postgres_transaction(postgres_connection):
    connection = postgres_connection

    with connection.begin() as transaction:
        yield connection

        transaction.rollback()


@pytest.fixture
def test_db_session(postgres_transaction):
    session_maker = sessionmaker(
        expire_on_commit=False, bind=postgres_transaction, autoflush=False
    )
    common_session_maker = scoped_session(session_maker)
    CommonSessionMaker().common_session_maker = common_session_maker

    yield common_session_maker

    CommonSessionMaker().common_session_maker = None


@pytest.yield_fixture(autouse=True)
def postgres_db_marker(request) -> None:
    """
    Initialize testing connection with postgres if test is marked with
    `postgres_db`. Assure that each test is run in a separate transaction.

    More technically: insert a Session factory into the Container which is [Session]
    connected to the test database. Note that a Session factory already exists in
    the Container (it got autodiscovered), but this Session goes first.

    If test is not marked then insert a Session-like factory which raises
    exception upon calling its attribute other than those that are required
    by the `transactional` decorator.

    In both cases remove the factory from the Container.
    """
    marker = request.keywords.get("postgres_db", None)
    if marker:
        request.getfixturevalue("postgres_db")

        engine = create_engine(TEST_DB_URL)
        connection = engine.connect()

        with connection.begin() as transaction:

            @egg(profile="tests")
            @scope(TRANSACTIONAL_SCOPE)
            def sql_alchemy_session_factory() -> Session:
                session_maker = sessionmaker(
                    expire_on_commit=False, bind=connection, autoflush=True
                )

                return cast(Session, session_maker())

            Container().config.insert(
                0, Egg(Session, None, None, sql_alchemy_session_factory)
            )

            yield

            Container().config.pop(0)
            transaction.rollback()
            connection.close()
            engine.dispose()

    else:

        def assertion_session_factory():
            class AssertionSession:
                def __getattr__(self, name):
                    if name not in ("commit", "close", "rollback"):
                        raise AssertionError(
                            "You cannot use DB in tests not marked by postgres_db"
                        )
                    else:
                        return lambda: None

            return AssertionSession()

        Container().config.insert(0, Egg(Session, None, None, assertion_session_factory))

        yield

        Container().config.pop(0)


@pytest.fixture
def db_session():
    return Container().get_object(Session)
