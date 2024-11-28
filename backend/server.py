from fastapi import FastAPI, Request
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///./sensors.db"
Base = declarative_base()


def get_engine():
    return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Define SensorData model
class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    sensor_type = Column(String, index=True)
    value = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()


@app.post("/api/sensor_data")
async def receive_sensor_data(request: Request):
    try:
        sensor_data = await request.json()
        sensor_type = sensor_data.get("sensor_type")
        value = sensor_data.get("value")

        # Store in the database
        db = SessionLocal()
        new_entry = SensorData(sensor_type=sensor_type, value=str(value))
        db.add(new_entry)
        db.commit()
        db.close()

        print(f"Stored {sensor_type} data: {value}")
        return {"status": "success"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
