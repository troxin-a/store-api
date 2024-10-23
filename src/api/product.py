from typing import List
from fastapi import Depends
from fastapi.routing import APIRouter
from config.db import get_db
from schemas.product import ProductBase, ProductRead
from schemas.users import UserRead
from services.product import product_create, product_list
from services.users import get_current_active_user

product_router = APIRouter(prefix="/product", tags=["Product"])

#################################################################################
#################################################################################
#################################################################################
#################################################################################
### А-А-А-А-А-А-А-А--А-А-А-А-А-АААААААААА Надо заполнить комменты и не комитить вообще!!!!
#################################################################################
#################################################################################
#################################################################################


@product_router.post("/")
async def create_product(
    product: ProductBase,
    user: UserRead = Depends(get_current_active_user),
    db=Depends(get_db),
) -> ProductRead:
    return await product_create(product, db)


@product_router.get("/")
async def list_product(
    user: UserRead = Depends(get_current_active_user),
    db=Depends(get_db),
) -> List[ProductRead]:    
    return await product_list(db)
