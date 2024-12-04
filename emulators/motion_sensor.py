import paho.mqtt.client as mqtt
import time
import random

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "home/motion"


# Callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    else:
        print(f"Failed to connect to MQTT broker, return code {rc}")


# Callback for when a message is published
def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully")


def main():
    # Create a new MQTT client instance with explicit protocol version
    client = mqtt.Client(protocol=mqtt.MQTTv311)

    # Set callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Connect to the MQTT broker
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()  # Start the network loop in a separate thread
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        return  # Exit if the connection fails

    try:
        while True:
            # Simulate motion data
            motion_detected = random.randint(0, 100)

            # Publish the data to the topic
            result = client.publish(MQTT_TOPIC, motion_detected)

            # Check for success
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Publishing motion data: {motion_detected}")
            else:
                print(f"Failed to publish motion data: {result.rc}")

            time.sleep(5)  # Publish data every 5 seconds
    except KeyboardInterrupt:
        print("\nStopping the emulator.")
    except Exception as e:
        print(f"Error during MQTT operation: {e}")
    finally:
        # Disconnect from the broker and stop the loop
        client.loop_stop()
        client.disconnect()
        print("Disconnected from the MQTT broker.")


if __name__ == "__main__":
    main()
