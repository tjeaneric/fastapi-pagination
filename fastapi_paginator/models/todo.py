from datetime import datetime
from typing import Union, Generic, TypeVar, List
from sqlmodel import SQLModel, Field
from sqlalchemy.sql import func

from sqlalchemy import DateTime, Column
from pydantic.generics import GenericModel

M = TypeVar('M')


class Todo(SQLModel, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(nullable=False, index=True)
    description: str = Field(nullable=False, index=True)
    done: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now,
                                 sa_column=Column(DateTime(timezone=True)), nullable=False)
    updated_at: Union[datetime, None] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))


class TodoSchema(SQLModel):
    id: int
    name: str
    description: Union[str, None]
    done: Union[bool, None]
    created_at: datetime


class PaginatedResponse(GenericModel, Generic[M]):
    count: int = Field(description='Total items before pagination')
    total_pages: int = Field(description='Number of pages depending on the page size')
    page_size: int = Field(description='Number of items returned in the response')
    page: int = Field(description='Current page number')
    data: List[M] = Field(description='List of items returned in the response following given criteria')
