import aiohttp
import asyncio
import random

HTTP_URL = "http://127.0.0.1:8001/humidity"


async def send_humidity_data():
    try:
        async with aiohttp.ClientSession() as session:
            print(f"Starting humidity sensor emulator, sending data to {HTTP_URL}")
            while True:
                humidity = 30 + (20 * random.random())  # Simulating random humidity
                payload = {"value": f"{humidity:.2f}"}

                try:
                    async with session.post(HTTP_URL, json=payload, timeout=5) as response:
                        if response.status == 200:
                            print(
                                f"Sent humidity data: {payload}, Response: {response.status}"
                            )
                        else:
                            print(
                                f"Failed to send data: {payload}, Response: {response.status}, {await response.text()}"
                            )
                except aiohttp.ClientError as req_err:
                    print(f"Request error: {req_err}")

                await asyncio.sleep(5)  # Send data every 5 seconds
    except asyncio.CancelledError:
        print("\nHumidity sensor task cancelled.")
    except Exception as e:
        print(f"Unexpected error: {e}")
