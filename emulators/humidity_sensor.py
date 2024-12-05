import aiohttp
import asyncio
import random
from logger import logger

HTTP_URL = "http://127.0.0.1:8001/humidity"


async def send_humidity_data():
    try:
        logger.info(f"Starting humidity sensor emulator, sending data to {HTTP_URL}")
        async with aiohttp.ClientSession() as session:
            while True:
                humidity = 30 + (20 * random.random())  # Simulating random humidity
                payload = {"value": f"{humidity:.2f}"}
                logger.debug(f"Generated humidity data: {payload}")

                try:
                    async with session.post(
                        HTTP_URL, json=payload, timeout=5
                    ) as response:
                        if response.status == 200:
                            logger.info(
                                f"Successfully sent humidity data: {payload}, Response: {response.status}"
                            )
                        else:
                            response_text = await response.text()
                            logger.warning(
                                f"Failed to send data: {payload}, Response: {response.status}, Message: {response_text}"
                            )
                except aiohttp.ClientError as req_err:
                    logger.error(
                        f"Request error while sending data: {payload}, Error: {req_err}"
                    )
                except asyncio.TimeoutError:
                    logger.error(f"Request timeout while sending data: {payload}")

                await asyncio.sleep(5)  # Send data every 5 seconds
    except asyncio.CancelledError:
        logger.info("Humidity sensor task cancelled.")
    except Exception as e:
        logger.error(
            f"Unexpected error occurred in humidity sensor emulator: {e}", exc_info=True
        )
