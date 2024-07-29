from fastapi import Depends
from sqlalchemy.orm import Session
from ..model.product_model import ProductModel
from ..configuration.database import get_db

def create_product_service(price: float, description: str, db: Session = Depends(get_db)):
    new_product = ProductModel(price=price, description=description)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def read_all_products_service(db: Session = Depends(get_db)):
    all_product = db.query(ProductModel).all()
    return all_product
