from fastapi import FastAPI, Query

from sqlalchemy import select

from database import create_db_and_tables, commonsDep
from fastapi_paginator.helpers import paginate

from models.todo import Todo, TodoSchema, PaginatedResponse
from contextlib import asynccontextmanager


#
#
@asynccontextmanager
async def initialize_todos(app: FastAPI):
    # Create Database tables on Startup
    create_db_and_tables()
    # with Session(engine) as session:
    #     for i in range(50):
    #         todo = Todo(name=str(i), description=f'task-{i}')
    #         session.add(todo)
    #     session.commit()
    # session.add_all([Todo(name=str(i), description=f'task-{i}') for i in range(50)])
    yield


app = FastAPI(lifespan=initialize_todos)


@app.get('/todos', response_model=PaginatedResponse[TodoSchema])
async def get_todos(q: commonsDep):
    return await paginate(select(Todo), q.page, q.per_page)
