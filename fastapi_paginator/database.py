from fastapi import Depends, Query

from sqlmodel import SQLModel, create_engine, Session
from typing_extensions import Annotated

from fastapi_paginator.config import settings

engine = create_engine(settings.db_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    """Create database session per request, close it after returning response"""
    with Session(engine) as session:
        yield session


# Database Session dependency
sessionDep = Annotated[Session, Depends(get_session)]


# Common Query Params like offset and limit
class CommonQueryParams:
    def __init__(self, page: Annotated[int, Query(ge=1)] = 1, per_page: Annotated[int, Query(ge=0, lte=100)] = 10):
        self.page = page
        self.per_page = per_page


commonsDep = Annotated[CommonQueryParams, Depends()]
