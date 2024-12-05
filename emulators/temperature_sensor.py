import asyncio
import random
from logger import logger

TCP_HOST = "127.0.0.1"
TCP_PORT_TEMP = 5001


async def send_temperature_data():
    try:
        logger.info(f"Attempting to connect to {TCP_HOST}:{TCP_PORT_TEMP}")
        reader, writer = await asyncio.open_connection(TCP_HOST, TCP_PORT_TEMP)
        logger.info(f"Connected to {TCP_HOST}:{TCP_PORT_TEMP}")

        while True:
            temperature = 25 + (5 * random.random())
            message = f"{temperature:.2f}\n"
            writer.write(message.encode("utf-8"))
            await writer.drain()
            logger.info(f"Sent temperature data: {message.strip()}")
            await asyncio.sleep(5)  # Send data every 5 seconds

    except ConnectionRefusedError:
        logger.error(
            f"Error: Unable to connect to {TCP_HOST}:{TCP_PORT_TEMP}. Ensure the server is running."
        )
    except Exception as e:
        logger.error(
            f"Unexpected error occurred in temperature data sender: {e}", exc_info=True
        )
    finally:
        if "writer" in locals() and not writer.is_closing():
            logger.info("Closing temperature data connection.")
            writer.close()
            await writer.wait_closed()
        logger.info("Temperature connection closed.")
