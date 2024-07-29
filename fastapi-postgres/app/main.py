from fastapi import FastAPI
from app.controller.product_controller import product_router

app = FastAPI(
    title="FastAPI and Postgres Dockerized 🐳", 
    description="https://github.com/docker/awesome-compose"
)

app.include_router(product_router)
