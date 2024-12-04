import asyncio
import random  # Import random module

TCP_HOST = "127.0.0.1"
TCP_PORT_TEMP = 5001


async def send_temperature_data():
    try:
        reader, writer = await asyncio.open_connection(TCP_HOST, TCP_PORT_TEMP)
        print(f"Connected to {TCP_HOST}:{TCP_PORT_TEMP}")

        while True:
            temperature = 25 + (5 * random.random())  # Simulating random temperature
            message = f"{temperature:.2f}\n"
            writer.write(message.encode("utf-8"))
            await writer.drain()
            print(f"Sent temperature data: {message.strip()}")
            await asyncio.sleep(5)  # Send data every 5 seconds

    except ConnectionRefusedError:
        print(
            f"Error: Unable to connect to {TCP_HOST}:{TCP_PORT_TEMP}. Ensure the server is running."
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if "writer" in locals() and not writer.is_closing():
            writer.close()
            await writer.wait_closed()
        print("Temperature connection closed.")
