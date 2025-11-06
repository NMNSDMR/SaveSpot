from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import uvicorn
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.database import add_location, init_db

app = FastAPI(title="Tracking Server")

class LocationData(BaseModel):
    tag_code: str
    lat: float
    lon: float

@app.on_event("startup")
async def startup():
    await init_db()

@app.post("/update_location")
async def update_location(data: LocationData):
    await add_location(data.tag_code, data.lat, data.lon)
    return {"status": "ok", "message": f"Location for {data.tag_code} saved."}

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
