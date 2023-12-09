# app/main.py
from fastapi import FastAPI
from app.database.session import create_db_and_tables

app = FastAPI()

# Create database tables
@app.on_event("startup")
async def on_startup():
    print("STARTUP", flush=True)
    await create_db_and_tables()

# Include API routes
# app.include_router(api_main.router)

# # Include FastAPI-Users routes
# app.include_router(fastapi_users.get_auth_router(models.Token, name="token"), prefix="/auth", tags=["auth"])
# app.include_router(fastapi_users.get_register_router(name="register"), prefix="/auth", tags=["auth"])
