from fastapi import FastAPI, Request

app = FastAPI(title="API on Linux")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get")
async def get_name(name:str):
    return {"name": name}
    
 