from typing import List
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
import dbconnect
import models

app = FastAPI(title="FastAPI calling PostgreSQL on Azure Linux Box")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(GZipMiddleware)

@app.on_event("startup")
async def startup():
    await dbconnect.database.connect()

@app.on_event("shutdown")
async def shutdown():
    await dbconnect.database.disconnect()

@app.post("/todo/", response_model=models.Todo, status_code = status.HTTP_201_CREATED)
async def create_todo(todo: models.TodoIn):
    query = dbconnect.todos.insert().values(text=todo.text, completed=todo.completed)
    last_record_id = await dbconnect.database.execute(query)
    return {**todo.dict(), "id": last_record_id}

@app.put("/todos/{todo_id}/", response_model=models.Todo, status_code = status.HTTP_200_OK)
async def update_todo(todo_id: int, payload: models.TodoIn):
    query = dbconnect.todos.update().where(dbconnect.todos.c.id == todo_id).values(text=payload.text, completed=payload.completed)
    await dbconnect.database.execute(query)
    return {**payload.dict(), "id": todo_id}

@app.get("/todos/", response_model=List[models.Todo], status_code = status.HTTP_200_OK)
async def read_todos(skip: int = 0, take: int = 20):
    query = dbconnect.todos.select().offset(skip).limit(take)
    return await dbconnect.database.fetch_all(query)

@app.get("/todos/{todo_id}/", response_model=models.Todo, status_code = status.HTTP_200_OK)
async def read_todos(todo_id: int):
    query = dbconnect.todos.select().where(dbconnect.todos.c.id == todo_id)
    return await dbconnect.database.fetch_one(query)

@app.delete("/todos/{todo_id}/", status_code = status.HTTP_200_OK)
async def delete_todo(todo_id: int):
    query = dbconnect.todos.delete().where(dbconnect.todos.c.id == todo_id)
    await dbconnect.database.execute(query)
    return {"message": "Todo with id: {} deleted successfully!".format(todo_id)}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastApi on Linux box [Azure]",
        version="1.0.0",
        description="Checking Fastapi connecting to PostGreSql in Azure App service Linux Box",
        routes=app.routes,
    )    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


