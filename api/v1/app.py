from typing import Optional

from fastapi import FastAPI

app = FastAPI(title="API Quimbaya",
              description="REST API for the administration of Scout groups",
              version="0.1.0"
              )


@app.get("/")
def read_root():
    return {"Hello": "World"}
