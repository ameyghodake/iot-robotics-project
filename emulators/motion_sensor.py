import paho.mqtt.client as mqtt
import time
import random

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "home/motion"


def main():
    # Create a new MQTT client instance
    client = mqtt.Client()

    # Connect to the MQTT broker
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        return  # Exit if the connection fails

    try:
        while True:
            # Simulate motion data
            motion_detected = random.choice(["motion_detected", "no_motion"])

            # Publish the data to the topic
            result = client.publish(MQTT_TOPIC, motion_detected)

            # Check for success
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Published motion data: {motion_detected}")
            else:
                print(f"Failed to publish motion data: {result.rc}")

            time.sleep(5)  # Publish data every 5 seconds
    except KeyboardInterrupt:
        print("\nStopping the emulator.")
    except Exception as e:
        print(f"Error during MQTT operation: {e}")
    finally:
        # Disconnect from the broker
        client.disconnect()
        print("Disconnected from the MQTT broker.")


if __name__ == "__main__":
    main()
