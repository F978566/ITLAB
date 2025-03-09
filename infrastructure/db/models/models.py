import os
from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from sqlalchemy.sql.sqltypes import UUID as SQLAlchemyUUID
import asyncio


class Base(AsyncAttrs, DeclarativeBase):
    pass


class TitleModel(Base):
    __tablename__ = "title"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    title: Mapped[str]

    full_titles: Mapped[List["FullTitleModel"]] = relationship(back_populates="title")
    

class FullTitleModel(Base):
    __tablename__ = "full_title"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    full_title: Mapped[str]

    problems: Mapped[List["ProblemModel"]] = relationship(back_populates="full_title")

    title_id: Mapped[UUID] = mapped_column(ForeignKey("title.id"))
    title: Mapped["TitleModel"] = relationship(back_populates="full_titles")
    

class ProblemModel(Base):
    __tablename__ = "problem"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    title_id: Mapped[UUID] = mapped_column(ForeignKey("full_title.id"))
    name: Mapped[str]
    description: Mapped[str]

    full_title: Mapped["FullTitleModel"] = relationship(back_populates="problems")
    
# engine = create_async_engine(
#     DATABASE_URL,
#     echo=True,  # Set to False in production
# )

# # Create async session factory
# AsyncSessionLocal = async_sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     autocommit=False,
#     autoflush=False,
#     expire_on_commit=False
# )

# # Base class for declarative models

# async def get_db() -> AsyncSession:
#     """Provide an async database session"""
#     async with AsyncSessionLocal() as session:
#         yield session
# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

# async def insert():
#     # async with get_db() as session:
#     async with AsyncSessionLocal() as session:
#         title = Title(title="Test Title")
#         title.problems = [
#             Problem(name="Problem 1", description="Problem 1 Description", title=title),
#             Problem(name="Problem 2", description="Problem 2 Description", title=title),
#         ]
#         session.add(title)
#         await session.commit()
        
        # problem = Problem(title=title, name="Test Problem", description="Test Description")
        # session.add(problem)
        # await session.commit()
        

# async def main():
#     await init_models()
#     await insert()
    
# asyncio.run(init_models())