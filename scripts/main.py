import subprocess
import time
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MONITOR = os.path.join(BASE_DIR, "monitor.py")
DEVICE = os.path.join(BASE_DIR, "device_monitor.py")

PYTHON = sys.executable

print("=" * 60)
print("AI NETWORK MONITOR")
print("=" * 60)

# Start both scripts
monitor_process = subprocess.Popen([PYTHON, MONITOR])
device_process = subprocess.Popen([PYTHON, DEVICE])

print("Network Monitor Started")
print("Device Monitor Started")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:

    print("\nStopping monitors...")

    monitor_process.terminate()
    device_process.terminate()

    monitor_process.wait()
    device_process.wait()

    print("Stopped Successfully.")