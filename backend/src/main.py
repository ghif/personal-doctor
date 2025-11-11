from fastapi import FastAPI
from src.api import query

app = FastAPI(
    title="Personal Doctor AI API",
    version="1.0.0",
)

app.include_router(query.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Personal Doctor AI API"}
