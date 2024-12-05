import asyncio
import random
from logger import logger

TCP_HOST = "127.0.0.1"
TCP_PORT_SMOKE = 5002


async def send_smoke_data():
    try:
        logger.info(f"Attempting to connect to {TCP_HOST}:{TCP_PORT_SMOKE}")
        reader, writer = await asyncio.open_connection(TCP_HOST, TCP_PORT_SMOKE)
        logger.info(f"Connected to {TCP_HOST}:{TCP_PORT_SMOKE}")

        while True:
            smoke_level = 10 + (5 * random.random())
            message = f"{smoke_level:.2f}\n"
            writer.write(message.encode("utf-8"))
            await writer.drain()
            logger.info(f"Sent smoke data: {message.strip()}")
            await asyncio.sleep(5)  # Send data every 5 seconds

    except ConnectionRefusedError:
        logger.error(
            f"Error: Unable to connect to {TCP_HOST}:{TCP_PORT_SMOKE}. Ensure the server is running."
        )
    except Exception as e:
        logger.error(
            f"Unexpected error occurred in smoke data sender: {e}", exc_info=True
        )
    finally:
        if "writer" in locals() and not writer.is_closing():
            logger.info("Closing smoke data connection.")
            writer.close()
            await writer.wait_closed()
        logger.info("Smoke connection closed.")
