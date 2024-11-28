import paho.mqtt.client as mqtt
import time
import random

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "home/motion"


def main():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")

    try:
        while True:
            motion_detected = random.choice(
                ["motion_detected", "no_motion"]
            )  # Simulating motion
            client.publish(MQTT_TOPIC, motion_detected)
            print(f"Published motion data: {motion_detected}")
            time.sleep(5)  # Publish data every 5 seconds
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
