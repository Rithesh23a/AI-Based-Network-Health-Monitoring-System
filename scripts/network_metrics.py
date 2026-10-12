import psutil
import speedtest
import subprocess
import time
from datetime import datetime

print("=" * 70)
print("        AI NETWORK HEALTH MONITOR")
print("=" * 70)

# --------------------------------------------------
# Timestamp
# --------------------------------------------------
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --------------------------------------------------
# CPU, RAM and Disk
# --------------------------------------------------
cpu = psutil.cpu_percent(interval=1)

ram = psutil.virtual_memory()

disk = psutil.disk_usage('/')

# --------------------------------------------------
# Internet Speed
# --------------------------------------------------
print("\nTesting Internet Speed...")

st = speedtest.Speedtest()

download = st.download()/1000000

upload = st.upload()/1000000

# --------------------------------------------------
# Ping
# --------------------------------------------------
ping = subprocess.run(
    ["ping","8.8.8.8","-n","4"],
    capture_output=True,
    text=True
)

output = ping.stdout

average_ping = "Unknown"

packet_loss = "0"

for line in output.split("\n"):

    if "Average =" in line:
        average_ping = line.split("Average =")[-1].strip()

    if "Lost =" in line:
        packet_loss = line.split("Lost =")[1].split("(")[0].strip()

# --------------------------------------------------
# Bandwidth
# --------------------------------------------------
net1 = psutil.net_io_counters()

time.sleep(1)

net2 = psutil.net_io_counters()

bytes_sent = net2.bytes_sent

bytes_recv = net2.bytes_recv

upload_bw = (net2.bytes_sent-net1.bytes_sent)*8/1000000

download_bw = (net2.bytes_recv-net1.bytes_recv)*8/1000000

# --------------------------------------------------
# Display
# --------------------------------------------------

print("\n")
print("="*70)

print("Timestamp :",timestamp)

print("="*70)

print("\n🖥 SYSTEM HEALTH")

print("-"*40)

print(f"CPU Usage          : {cpu}%")

print(f"RAM Usage          : {ram.percent}%")

print(f"Disk Usage         : {disk.percent}%")

print("\n🌐 INTERNET")

print("-"*40)

print(f"Download Speed     : {download:.2f} Mbps")

print(f"Upload Speed       : {upload:.2f} Mbps")

print(f"Ping               : {average_ping}")

print(f"Packet Loss        : {packet_loss}")

print("\n📊 BANDWIDTH")

print("-"*40)

print(f"Bytes Sent         : {bytes_sent}")

print(f"Bytes Received     : {bytes_recv}")

print(f"Upload Bandwidth   : {upload_bw:.2f} Mbps")

print(f"Download Bandwidth : {download_bw:.2f} Mbps")

print("\n")
print("="*70)
print("Network Metrics Collected Successfully")
print("="*70)