from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.users import users_router
from api.base import base_router
from api.product import product_router
from api.cart import cart_router
from config.settings import Settings


app = FastAPI(**Settings().model_dump())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=("GET", "POST"),
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(base_router)
app.include_router(product_router)
app.include_router(cart_router)
