import asyncio
import aiohttp
import paho.mqtt.client as mqtt
from fastapi import FastAPI, Request
import uvicorn

# Backend API endpoint
BACKEND_API_URL = "http://127.0.0.1:8000/api/sensor_data"

# TCP host and ports
TCP_HOST = "127.0.0.1"
TCP_PORT_TEMP = 6001
TCP_PORT_SMOKE = 6002

# MQTT broker settings
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "home/motion"

app = FastAPI()
mqtt_data_queue = asyncio.Queue()


# MQTT client setup
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    asyncio.get_event_loop().call_soon_threadsafe(
        asyncio.create_task, mqtt_data_queue.put(("motion", payload))
    )


async def mqtt_listener():
    client = mqtt.Client()
    client.on_message = on_message
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.subscribe(MQTT_TOPIC)
        client.loop_start()
        print("[INFO] MQTT listener started")
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"[ERROR] MQTT connection failed: {e}")


async def tcp_listener(port, sensor_type):
    try:
        server = await asyncio.start_server(
            lambda reader, writer: handle_tcp_connection(reader, writer, sensor_type),
            TCP_HOST,
            port,
        )
        print(f"[INFO] TCP listener started on port {port} for {sensor_type}")
        async with server:
            await server.serve_forever()
    except Exception as e:
        print(f"[ERROR] Failed to start TCP listener on port {port}: {e}")


async def handle_tcp_connection(reader, writer, sensor_type):
    try:
        while data := await reader.readline():
            decoded_data = data.decode("utf-8").strip()
            print(f"[TCP] {sensor_type}: {decoded_data}")
            await send_to_backend(sensor_type, decoded_data)
    except Exception as e:
        print(f"[TCP] Connection error for {sensor_type}: {e}")


@app.post("/humidity")
async def receive_humidity(request: Request):
    try:
        humidity_data = await request.json()
        print(f"[HTTP] Humidity: {humidity_data}")
        await send_to_backend("humidity", humidity_data)
    except Exception as e:
        print(f"[HTTP] Error processing humidity data: {e}")
    return {"status": "success"}


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


async def process_mqtt_queue():
    while True:
        sensor_type, value = await mqtt_data_queue.get()
        await send_to_backend(sensor_type, value)
        mqtt_data_queue.task_done()


async def main():
    await asyncio.gather(
        mqtt_listener(),
        tcp_listener(TCP_PORT_TEMP, "temperature"),
        tcp_listener(TCP_PORT_SMOKE, "smoke"),
        process_mqtt_queue(),
    )


if __name__ == "__main__":
    print("Starting middleware server...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
