from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.auth import auth_routers
from app.routers.games import games_router
from app.routers.cart import cart_router
from app.routers.users import users_router
from app.services.auth import create_adm

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_adm()
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(auth_routers)
app.include_router(cart_router)
app.include_router(games_router)
app.include_router(users_router)

