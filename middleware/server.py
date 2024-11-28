import asyncio
import aiohttp
import socket
import paho.mqtt.client as mqtt
from fastapi import FastAPI, Request
import uvicorn

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
            print(f"[TCP] {sensor_type}: {decoded_data}")
            await send_to_backend(sensor_type, decoded_data)
    except Exception as e:
        print(f"[TCP] Connection error for {sensor_type}: {e}")
    finally:
        writer.close()


async def tcp_listener(port, sensor_type):
    try:
        print(f"Starting TCP listener for {sensor_type} on {TCP_HOST}:{port}")
        server = await asyncio.start_server(
            lambda r, w: handle_tcp_connection(r, w, sensor_type),
            TCP_HOST,
            port,
        )
        async with server:
            await server.serve_forever()
    except Exception as e:
        print(f"[TCP] Failed to start {sensor_type} listener: {e}")


# MQTT Handlers
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    asyncio.create_task(mqtt_data_queue.put(("motion", payload)))


async def mqtt_listener():
    try:
        client = mqtt.Client()
        client.on_message = on_message
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.subscribe(MQTT_TOPIC)
        client.loop_start()
        print(f"[MQTT] Listening to topic: {MQTT_TOPIC}")
        while True:
            sensor_type, value = await mqtt_data_queue.get()
            print(f"[MQTT] Received {sensor_type} data: {value}")
            await send_to_backend(sensor_type, value)
    except Exception as e:
        print(f"[MQTT] Error: {e}")


# HTTP Handlers
@app.post("/humidity")
async def receive_humidity(request: Request):
    try:
        humidity_data = await request.json()
        print(f"[HTTP] Received humidity data: {humidity_data}")
        await send_to_backend("humidity", humidity_data["value"])
        return {"status": "success"}
    except Exception as e:
        print(f"[HTTP] Error handling humidity data: {e}")
        return {"status": "error", "message": str(e)}


# Backend Communication
async def send_to_backend(sensor_type, value):
    async with aiohttp.ClientSession() as session:
        payload = {"sensor_type": sensor_type, "value": value}
        try:
            async with session.post(BACKEND_API_URL, json=payload) as response:
                print(
                    f"[Backend] Sent {sensor_type} data: {value}, Response: {response.status}"
                )
        except Exception as e:
            print(f"[Backend] Error sending {sensor_type} data: {e}")


# Main Coroutine
async def main():
    await asyncio.gather(
        mqtt_listener(),
        tcp_listener(TCP_PORT_TEMP, "temperature"),
        tcp_listener(TCP_PORT_SMOKE, "smoke"),
    )


if __name__ == "__main__":
    print("Starting middleware server...")
    # Run FastAPI on a separate thread
    asyncio.create_task(uvicorn.run(app, host="127.0.0.1", port=8001))
    # Start all listeners
    asyncio.run(main())