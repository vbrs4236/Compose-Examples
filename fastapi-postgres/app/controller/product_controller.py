from fastapi import APIRouter, Depends
from ..configuration.database import get_db
from sqlalchemy.orm import Session

from ..service.product_service import (
    create_product_service, read_all_products_service
)

product_router = APIRouter(prefix="/products", tags=["Products"])

@product_router.get("/get-all/")
def get_read_all_products_controller(db: Session = Depends(get_db)):
    return read_all_products_service(db)


@product_router.post("/create")
def post_create_product_controller(price:float, description:str, db: Session = Depends(get_db)):
    return create_product_service(price, description, db)
