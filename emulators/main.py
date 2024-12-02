import subprocess
import os


def run_emulator(script_name):
    # Build the absolute path for the emulator script
    emulator_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(emulator_path):
        raise FileNotFoundError(f"Emulator script not found: {emulator_path}")
    return subprocess.Popen(["python", emulator_path])


if __name__ == "__main__":
    emulators = [
        # "temperature_sensor.py",
        "smoke_sensor.py",
        "humidity_sensor.py",
        # "motion_sensor.py",
    ]

    processes = []
    try:
        for emulator in emulators:
            print(f"Starting {emulator}...")
            process = run_emulator(emulator)
            processes.append(process)

        # Wait for all processes and print any output
        for process in processes:
            stdout, stderr = process.communicate()
            if stdout:
                print(f"Output from {emulator}: {stdout.decode()}")
            if stderr:
                print(f"Error from {emulator}: {stderr.decode()}")

    except KeyboardInterrupt:
        print("\nTerminating all emulators...")
        for process in processes:
            process.terminate()
