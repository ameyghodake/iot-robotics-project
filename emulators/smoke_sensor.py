import asyncio
import random  # Import random module

TCP_HOST = "127.0.0.1"
TCP_PORT_SMOKE = 5002


async def send_smoke_data():
    try:
        reader, writer = await asyncio.open_connection(TCP_HOST, TCP_PORT_SMOKE)
        print(f"Connected to {TCP_HOST}:{TCP_PORT_SMOKE}")

        while True:
            smoke_level = 10 + (5 * random.random())  # Simulating random smoke levels
            message = f"{smoke_level:.2f}\n"
            writer.write(message.encode("utf-8"))
            await writer.drain()
            print(f"Sent smoke data: {message.strip()}")
            await asyncio.sleep(5)  # Send data every 5 seconds

    except ConnectionRefusedError:
        print(
            f"Error: Unable to connect to {TCP_HOST}:{TCP_PORT_SMOKE}. Ensure the server is running."
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if "writer" in locals() and not writer.is_closing():
            writer.close()
            await writer.wait_closed()
        print("Smoke connection closed.")
