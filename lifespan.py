from contextlib import asynccontextmanager
from models import init_orm, close_orm
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_orm()
    yield
    await close_orm()