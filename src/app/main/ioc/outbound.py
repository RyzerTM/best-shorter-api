import logging
from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.main.config.settings import PostgresSettings, SqlaSettings

logger = logging.getLogger(__name__)


class PersistenceSqlaProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_async_engine(
        self,
        postgres: PostgresSettings,
        sqla: SqlaSettings,
    ) -> AsyncIterator[AsyncEngine]:
        async_engine = create_async_engine(
            url=postgres.dsn,
            echo=sqla.echo,
            echo_pool=sqla.echo_pool,
            pool_size=sqla.pool_size,
            max_overflow=sqla.max_overflow,
            connect_args={"connect_timeout": 5},
            pool_pre_ping=True,
        )
        logger.debug("Async engine created with DSN: %s", postgres.dsn)
        yield async_engine
        logger.debug("Disposing async engine...")
        await async_engine.dispose()
        logger.debug("Async engine disposed.")

    @provide(scope=Scope.APP)
    async def async_session_factory(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        async_session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )
        logger.debug("Async session maker initialized.")
        return async_session_factory

    @provide(scope=Scope.REQUEST)
    async def provide_primary_async_session(
        self,
        async_session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:
        logger.debug("Starting Primary async session...")
        async with async_session_factory() as session:
            logger.debug("Primary async session started.")
            yield session
            logger.debug("Closing Primary async session...")
        logger.debug("Primary async session closed.")
