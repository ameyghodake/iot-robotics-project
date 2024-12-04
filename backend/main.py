from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import SessionLocal, init_db
from .models import SensorData

# Initialize database
try:
    init_db()
except Exception as e:
    print(e)


app = FastAPI()


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic model for data input
class SensorDataInput(BaseModel):
    sensor_type: str
    value: float


# Endpoint to receive sensor data
@app.post("/api/sensor_data")
async def receive_sensor_data(data: SensorDataInput, db: Session = Depends(get_db)):
    sensor_data = SensorData(sensor_type=data.sensor_type, value=data.value)
    db.add(sensor_data)
    db.commit()
    db.refresh(sensor_data)
    return {"status": "success", "data": {"id": sensor_data.id}}


# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "ok"}
