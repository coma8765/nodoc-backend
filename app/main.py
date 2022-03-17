from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import views
from app import dependencies
from app.models.base import Base

app = FastAPI()

app.include_router(views.router)


origins = [
    "*",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await dependencies.startup()
    Base.metadata.create_all(dependencies.engine)


@app.on_event("shutdown")
async def startup():
    await dependencies.shutdown()


app.middleware("http")(views.exc.exception_handler)
