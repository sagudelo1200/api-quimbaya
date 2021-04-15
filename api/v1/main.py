from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routers import router

app = FastAPI(title='API Quimbaya',
              description='REST API for the administration of Scout groups',
              version='0.1.0',
              )

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_headers=['*']
)

@app.get('/')
def read_root():
    return {'resourse': app.title, 'status': 'OK', 'version': app.version}
