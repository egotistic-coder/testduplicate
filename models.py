from pydantic.main import BaseModel
from sqlalchemy.sql.sqltypes import Date


class TodoIn(BaseModel):
    text: str
    completed: bool

class Todo(BaseModel):
    id: int
    text: str
    completed: bool


