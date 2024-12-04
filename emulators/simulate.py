import asyncio
from .temperature_sensor import send_temperature_data
from .smoke_sensor import send_smoke_data
from .humidity_sensor import send_humidity_data


async def main():
    # Run both tasks concurrently
    await asyncio.gather(
        send_temperature_data(),
        send_smoke_data(),
        send_humidity_data(),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Sensor emulation stopped.")
