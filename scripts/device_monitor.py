import nmap
import sqlite3
import subprocess
import re
from datetime import datetime
import os
import time

# -----------------------------------
# Configuration
# -----------------------------------

NETWORK = " 172.20.230.250/24"

DB_PATH = r"C:\Users\Vishwa\Desktop\AI_NETWORK_MONITOR\data\network.db"


# -----------------------------------
# Get Ping & Packet Loss
# -----------------------------------

def get_ping(ip):

    try:

        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", ip],
            capture_output=True,
            text=True,
            timeout=3
        )

        output = result.stdout

        ping = 999
        packet_loss = 100

        # Ping

        match = re.search(r"Average = (\d+)ms", output)

        if match:
            ping = float(match.group(1))

        else:
            match = re.search(r"time[=<](\d+)ms", output)

            if match:
                ping = float(match.group(1))

        # Packet Loss

        match = re.search(r"\((\d+)% loss\)", output)

        if match:
            packet_loss = int(match.group(1))

        return ping, packet_loss

    except Exception as e:

        print("Ping Error :", ip, e)

        return 999, 100


# -----------------------------------
# Health Score
# -----------------------------------

def calculate_health(ping, loss):

    score = 100

    if ping > 100:
        score -= 30

    elif ping > 50:
        score -= 15

    score -= loss

    if score < 0:
        score = 0

    return score


# -----------------------------------
# Main
# -----------------------------------

print("=" * 70)
print("DEVICE MONITOR")
print("=" * 70)

try:
    while True:
        print("Creating Scanner...")

        scanner = nmap.PortScanner()

        print("Scanning Network...")

        scanner.scan(hosts=NETWORK, arguments="-sn")

        hosts = scanner.all_hosts()

        print(f"Devices Found : {len(hosts)}")

        print("Opening Database...")



        print("\nDatabase Path:")
        print(DB_PATH)
        print("Exists:", os.path.exists(DB_PATH))

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()


        cursor.execute("DELETE FROM device_metrics")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='device_metrics'")
        conn.commit()

        print("-" * 70)

        print("{:<18} {:<20} {:<10} {:<10} {:<10}".format(
            "IP",
            "Hostname",
            "Ping",
            "Loss",
            "Health"
        ))

        print("-" * 70)

        for host in hosts:

            print("Checking :", host)

            hostname = scanner[host].hostname()

            if hostname == "":
                hostname = "Unknown"

            status = scanner[host].state()

            ping, loss = get_ping(host)

            health = calculate_health(ping, loss)

            print("{:<18} {:<20} {:<10} {:<10} {:<10}".format(
                host,
                hostname,
                str(ping),
                str(loss) + "%",
                health
            ))

            cursor.execute("""

                INSERT INTO device_metrics(

                    timestamp,

                    ip,

                    hostname,

                    status,

                    ping,

                    packet_loss,

                    health_score

                )

                VALUES(?,?,?,?,?,?,?)

            """, (

                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                host,

                hostname,

                status,

                ping,

                loss,

                health

            ))

            print(f"Inserted {host}")
        cursor.execute("SELECT COUNT(*) FROM device_metrics")
        print("Rows currently in table:", cursor.fetchone()[0])
        conn.commit()


        conn.commit()
        cursor.execute("SELECT COUNT(*) FROM device_metrics")
        print("Final rows:", cursor.fetchone()[0])
        conn.close()

        print("-" * 70)
        print("All Devices Saved Successfully!")
        print("=" * 70)
        print("Waiting 5 seconds...\n")
        time.sleep(5)

except KeyboardInterrupt:
    print("\nDevice Monitor Stopped.")