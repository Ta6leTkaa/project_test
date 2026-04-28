from fastapi import FastAPI, HTTPException
from app.api.v1.wallets import router as wallet_router
from app.api.v1.operations import router as operations_router
from app.api.v1.users import router as users_router
from app.database import Base, engine

app = FastAPI()

app.include_router(wallet_router, prefix="/api/v1", tags = ["Wallet"])
app.include_router(operations_router, prefix="/api/v1", tags = ["Operations"])
app.include_router(users_router, prefix="/api/v1", tags = ["Users"])

Base.metadata.create_all(bind=engine)
