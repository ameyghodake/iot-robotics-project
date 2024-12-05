from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import SessionLocal, init_db
from .models import SensorData
from logger import logger

# Initialize database
try:
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing database: {e}", exc_info=True)

app = FastAPI()


# Dependency for database session
def get_db():
    logger.debug("Creating a new database session.")
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.debug("Closing the database session.")
        db.close()


# Pydantic model for data input
class SensorDataInput(BaseModel):
    sensor_type: str
    value: float


# Endpoint to receive sensor data
@app.post("/api/sensor_data")
async def receive_sensor_data(data: SensorDataInput, db: Session = Depends(get_db)):
    logger.info(f"Received sensor data: {data}")
    try:
        sensor_data = SensorData(sensor_type=data.sensor_type, value=data.value)
        db.add(sensor_data)
        db.commit()
        db.refresh(sensor_data)
        logger.info(f"Sensor data saved successfully with ID: {sensor_data.id}")
        return {"status": "success", "data": {"id": sensor_data.id}}
    except Exception as e:
        logger.error(f"Error saving sensor data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to save sensor data")


# Health check endpoint
@app.get("/")
async def health_check():
    logger.info("Health check endpoint called.")
    return {"status": "ok"}
