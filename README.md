# Smart Home Integration Project

This project provides a complete smart home system with multiple sensor emulators, a middleware server, and a backend service for data handling. The system communicates with different sensor types (motion, temperature, humidity, smoke, and CO detectors) and stores data in a database. The middleware forwards data from the sensors to the backend, where it is processed and stored. The project is designed to be run asynchronously for easy setup and scalability.


## Prerequisites

Ensure you have the following installed:
- **pgAdmin4** (Postgres SQL Database)
- **Python 3.9+** (optional, for local development).
- **Graphana** (Visualisation tool [Results added in results folder in the repo])

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ameyghodake/iot-robotics-project.git
   cd iot-robotics-project

2. **Installing the dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Starting the backend server [start each server in separate terminal window]**:
   ```bash
   uvicorn backend.main:app --reload

4. **Starting the middleware server**:
   ```bash
   python -m middleware.server

5. **Starting the emulator server**:
   ```bash
   python -m emulators.simulate

6. **You need to update the postgres id password URL from backend.database file**

# Project Components
## Backend
1. Handles incoming data from sensors.
2. Stores sensor data in a PostgreSQL database.
3. Exposes an API for data retrieval and management.

### Key Files
1. backend/main.py: The entry point for the backend server. It runs the FastAPI or Django application, setting up API routes and managing requests.
2. backend/database.py: Handles the connection to the PostgreSQL database and provides methods for data insertion, querying, and other database operations.
3. backend/models.py: Defines the database schema and models for storing sensor data. This can include classes for different types of sensor data, each mapped to specific database tables.

## Sensor Emulator
1. Simulates real sensor data using different communication protocols (MQTT, TCP, HTTP).
2. Each sensor emulator runs as a separate Python script that publishes data to the middleware.

### Key Files
1. sensor_emulator/motion_sensor.py: Simulates motion sensor data and sends updates via MQTT (Message Queuing Telemetry Transport) protocol.
2. sensor_emulator/temperature_sensor.py: Simulates temperature sensor data and sends updates via a TCP socket connection.
3. sensor_emulator/humidity_sensor.py: Simulates humidity sensor data and communicates using HTTP requests.
4. sensor_emulator/smoke_sensor.py: Simulates smoke and CO detector data using a TCP socket connection.
5. sensor_emulator/simulate.py: A script that orchestrates the execution of individual sensor emulators. This script could be used for testing all emulators simultaneously.

## Middleware
1. Listens to data streams from all sensor emulators.
2. Forwards data to the backend for processing and storage.

### Key Files
1. middleware/server.py: The main script for the middleware server. It establishes connections with sensor emulators and forwards data to the backend using API calls.

## Graphana Dashboards
[text](README.md) ![text](results/smoke.png)
![alt text](results/humidity.png)
![alt text](results/temperature.png)

## Troubleshooting
1. Running logs can verified after running the server in logs folder which will be created after start

## License
This project is licensed under the MIT License. See the LICENSE file for details.
