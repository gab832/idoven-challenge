from fastapi import FastAPI

from authentication.routers import routers as auth_routers
from ecg.routers import routers as ecg_routers
from database import initialize_db

app = FastAPI()

@app.on_event('startup')
async def startup_event():
    initialize_db()

app.include_router(auth_routers)
app.include_router(ecg_routers)
