import databases
import sqlalchemy
import config

database = databases.Database(config.DATABASE_URL)

metadata = sqlalchemy.MetaData()

todos = sqlalchemy.Table(
    "todos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(    
    config.DATABASE_URL, pool_size=3, max_overflow=0
)

metadata.create_all(engine)