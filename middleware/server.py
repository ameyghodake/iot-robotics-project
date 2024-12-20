import asyncio
import aiohttp
import threading
import paho.mqtt.client as mqtt
from fastapi import FastAPI, Request
import uvicorn
from logger import logger

# Configuration
TCP_HOST = "127.0.0.1"
TCP_PORT_TEMP = 5001
TCP_PORT_SMOKE = 5002

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "home/motion"

BACKEND_API_URL = "http://127.0.0.1:8000/api/sensor_data"

# FastAPI App
app = FastAPI()
mqtt_data_queue = asyncio.Queue()


# TCP Handlers
async def handle_tcp_connection(reader, writer, sensor_type):
    try:
        while data := await reader.readline():
            decoded_data = data.decode("utf-8").strip()
            logger.info(f"[TCP] {sensor_type}: Received data: {decoded_data}")
            await send_to_backend(sensor_type, decoded_data)
    except Exception as e:
        logger.error(f"[TCP] Connection error for {sensor_type}: {e}", exc_info=True)
    finally:
        writer.close()
        await writer.wait_closed()
        logger.info(f"[TCP] Connection closed for {sensor_type}")


async def tcp_listener(port, sensor_type):
    try:
        logger.info(f"Starting TCP listener for {sensor_type} on {TCP_HOST}:{port}")
        server = await asyncio.start_server(
            lambda r, w: handle_tcp_connection(r, w, sensor_type),
            TCP_HOST,
            port,
        )
        async with server:
            await server.serve_forever()
    except Exception as e:
        logger.error(
            f"[TCP] Failed to start {sensor_type} listener: {e}", exc_info=True
        )


# MQTT Handlers
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    logger.info(f"[MQTT] Received message on topic {message.topic}: {payload}")
    asyncio.run_coroutine_threadsafe(
        mqtt_data_queue.put(("motion", payload)), asyncio.get_running_loop()
    )


async def mqtt_listener():
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_message = on_message
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.subscribe(MQTT_TOPIC)
        client.loop_start()
        logger.info(f"[MQTT] Listening to topic: {MQTT_TOPIC}")

        while True:
            sensor_type, value = await mqtt_data_queue.get()
            logger.info(f"[MQTT] Processing {sensor_type} data: {value}")
            await send_to_backend(sensor_type, value)
    except Exception as e:
        logger.error(f"[MQTT] Error: {e}", exc_info=True)


# HTTP Handlers
@app.post("/humidity")
async def receive_humidity(request: Request):
    try:
        humidity_data = await request.json()
        logger.info(f"[HTTP] Received humidity data: {humidity_data}")
        await send_to_backend("humidity", humidity_data["value"])
        return {"status": "success"}
    except Exception as e:
        logger.error(f"[HTTP] Error handling humidity data: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


# Backend Communication
async def send_to_backend(sensor_type, value):
    async with aiohttp.ClientSession() as session:
        payload = {"sensor_type": sensor_type, "value": value}
        try:
            async with session.post(BACKEND_API_URL, json=payload) as response:
                logger.info(
                    f"[Backend] Sent {sensor_type} data: {value}, Response: {response.status}"
                )
        except Exception as e:
            logger.error(
                f"[Backend] Error sending {sensor_type} data: {e}", exc_info=True
            )


# Main Coroutine
async def start_middleware():
    # Start all listeners concurrently
    logger.info("Starting middleware...")
    await asyncio.gather(
        mqtt_listener(),
        tcp_listener(TCP_PORT_TEMP, "temperature"),
        tcp_listener(TCP_PORT_SMOKE, "smoke"),
    )


# Start FastAPI and Middleware
if __name__ == "__main__":
    # Run FastAPI in a separate thread
    def run_uvicorn():
        logger.info("Starting FastAPI server...")
        uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")

    # Start FastAPI server in a thread
    threading.Thread(target=run_uvicorn, daemon=True).start()

    # Start asyncio event loop for middleware
    logger.info("Starting asyncio event loop for middleware...")
    asyncio.run(start_middleware())
