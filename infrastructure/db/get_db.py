from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from infrastructure.db.config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Base class for declarative models

async def get_db() -> AsyncSession:
    """Provide an async database session"""
    async with AsyncSessionLocal() as session:
        yield session