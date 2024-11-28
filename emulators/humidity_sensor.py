import requests
import time
import random

HTTP_URL = "http://127.0.0.1:8001/humidity"


def main():
    try:
        print(f"Starting humidity sensor emulator, sending data to {HTTP_URL}")
        while True:
            humidity = 30 + (20 * random.random())  # Simulating random humidity
            payload = {"value": f"{humidity:.2f}"}

            try:
                response = requests.post(
                    HTTP_URL, json=payload, timeout=5
                )  # Set timeout for request
                if response.status_code == 200:
                    print(
                        f"Sent humidity data: {payload}, Response: {response.status_code}"
                    )
                else:
                    print(
                        f"Failed to send data: {payload}, Response: {response.status_code}, {response.text}"
                    )
            except requests.exceptions.RequestException as req_err:
                print(f"Request error: {req_err}")

            time.sleep(4)  # Send data every 4 seconds
    except KeyboardInterrupt:
        print("\nHumidity sensor emulator stopped.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
