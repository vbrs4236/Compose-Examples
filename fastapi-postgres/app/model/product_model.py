from sqlalchemy import Column, Integer, String, Float
from ..configuration.database import Base, engine

class ProductModel(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    price = Column(Float)
    description = Column(String)

    def __init__(self, product_name, price, description):
        self.product_name = product_name
        self.price = price
        self.description = description

Base.metadata.create_all(bind = engine)
