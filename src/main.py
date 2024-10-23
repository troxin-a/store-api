from fastapi import FastAPI
from api.users import users_router
from api.base import base_router
from api.product import product_router
from models.cart_product import CartProduct
from models.cart import Cart


app = FastAPI()

app.include_router(users_router)
app.include_router(base_router)
app.include_router(product_router)
