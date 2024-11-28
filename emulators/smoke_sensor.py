import asyncio
import random  # Import random module

TCP_HOST = "127.0.0.1"
TCP_PORT_SMOKE = 5002


async def send_smoke_data():
    reader, writer = await asyncio.open_connection(TCP_HOST, TCP_PORT_SMOKE)
    print(f"Connected to {TCP_HOST}:{TCP_PORT_SMOKE}")

    try:
        while True:
            smoke_level = 10 + (5 * random.random())  # Simulating random smoke levels
            message = f"{smoke_level:.2f}\n"
            writer.write(message.encode("utf-8"))
            await writer.drain()
            print(f"Sent smoke data: {message.strip()}")
            await asyncio.sleep(3)  # Send data every 3 seconds
    except Exception as e:
        print(f"Error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()


asyncio.run(send_smoke_data())
