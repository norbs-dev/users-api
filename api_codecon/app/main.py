import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.routes import router
from app.db.connection import Base, engine, DB_FILE

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    Base.metadata.create_all(bind=engine)
    print("Temporary database created.")
    yield
    # Shutdown logic
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Temporary database {DB_FILE} deleted on shutdown.")

#Base.metadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)
app.include_router(router)