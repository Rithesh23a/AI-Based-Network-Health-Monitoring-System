from utils import *
import sqlite3
from datetime import datetime
from ai_model import calculate_health
import time
import joblib

model = joblib.load("C:/Users/Vishwa/Desktop/AI_NETWORK_MONITOR/model/network_model.pkl")
def monitor_network(devices):


    print("=" * 60)
    print("      AI POWERED PREDICTIVE NETWORK HEALTH MONITOR")
    print("=" * 60)

# -----------------------------
# Collect System Metrics
# -----------------------------
    cpu, ram, disk = get_system_metrics()

# -----------------------------
# Collect Internet Speed
# -----------------------------
    download, upload, ping = get_speed()

# -----------------------------
# Collect Packet Loss
# -----------------------------
    ping, packet_loss = get_ping()

# -----------------------------
# Collect Bandwidth
# -----------------------------
    bytes_sent, bytes_received, upload_bw, download_bw = get_bandwidth()
    jitter = get_jitter()

    health_score = calculate_health(
        download,
        upload,
        ping,
        packet_loss,
        jitter,
        download_bw,
        devices
    )
    prediction = model.predict([[download,
                                upload,
                                ping,
                                packet_loss,
                                jitter,
                                download_bw,
                                devices
                                ]])[0]

    conn = sqlite3.connect("C:/Users/Vishwa/Desktop/AI_NETWORK_MONITOR/data/network.db")
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# -----------------------------
# Display Results
# -----------------------------

    print("\nSYSTEM HEALTH")
    print("-" * 30)
    print(f"CPU Usage           : {cpu:.1f} %")
    print(f"RAM Usage           : {ram:.1f} %")
    print(f"Disk Usage          : {disk:.1f} %")

    print("\nINTERNET SPEED")
    print("-" * 30)
    print(f"Download Speed      : {download:.2f} Mbps")
    print(f"Upload Speed        : {upload:.2f} Mbps")
    print(f"Ping                : {ping:.2f} ms")
    print(f"Packet Loss         : {packet_loss}")

    print("\nBANDWIDTH")
    print("-" * 30)
    print(f"Bytes Sent          : {bytes_sent}")
    print(f"Bytes Received      : {bytes_received}")
    print(f"Upload Bandwidth    : {upload_bw:.2f} Mbps")
    print(f"Download Bandwidth  : {download_bw:.2f} Mbps")

    print("\nCONNECTED DEVICES")
    print("-" * 30)
    print(f"Devices Connected   : {devices}")

    print("\nAI NETWORK HEALTH")
    print("-"*30)
    print(f"Health Score : {health_score}/100")
    print(f"Prediction :{prediction}")
    print(f"Jitter : {jitter} ms")

    print("\n" + "=" * 60)
    print("Network Monitoring Completed Successfully")
    print("=" * 60)
    cursor.execute("""
    INSERT INTO network_metrics
    (
        timestamp,
        cpu,
        ram,
        disk,
        download_speed,
        upload_speed,
        ping,
        packet_loss,
        bytes_sent,
        bytes_received,
        upload_bandwidth,
        download_bandwidth,
        connected_devices,
        health_score,
        prediction
    )
    VALUES
    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """,
    (
        timestamp,
        cpu,
        ram,
        disk,
        download,
        upload,
        ping,
        packet_loss,
        bytes_sent,
        bytes_received,
        upload_bw,
        download_bw,
        devices,
        health_score,
        prediction
    ))

    print("\nSaving data to database...")

    conn.commit()

    print("Commit Successful!")

    cursor.execute("SELECT COUNT(*) FROM network_metrics")
    total = cursor.fetchone()[0]

    print(f"Total Rows in network_metrics : {total}")

    cursor.execute("""
        SELECT id,
               cpu,
               ram,
               disk,
               download_speed,
               upload_speed
        FROM network_metrics
        ORDER BY id DESC
        LIMIT 1
    """)

    latest = cursor.fetchone()

    print("Latest Record :", latest)

    conn.close()

    print("\nData Saved Successfully!")


# --------------------------------
# Run continuously
# --------------------------------

device_counter = 0
devices = 0

while True:

    # Scan connected devices only once every minute
    if device_counter == 0:
        devices = get_connected_devices()

    monitor_network(devices)

    device_counter += 1

    if device_counter == 12:
        device_counter = 0

    print("\nWaiting 5 seconds...\n")
    time.sleep(5)