import psutil
import netifaces
import nmap

def get_system_metrics():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    return cpu, ram, disk
import time

def get_bandwidth():

    net1 = psutil.net_io_counters()

    time.sleep(1)

    net2 = psutil.net_io_counters()

    upload_bw = (net2.bytes_sent-net1.bytes_sent)*8/1000000

    download_bw = (net2.bytes_recv-net1.bytes_recv)*8/1000000

    return (
        net2.bytes_sent,
        net2.bytes_recv,
        upload_bw,
        download_bw
    )


import subprocess
import re

def get_speed():

    result = subprocess.run(
        ["speedtest-cli", "--simple"],
        capture_output=True,
        text=True
    )

    output = result.stdout

    download = 0
    upload = 0
    ping = 0

    for line in output.splitlines():

        if "Ping" in line:
            ping = float(re.findall(r"[\d.]+", line)[0])

        elif "Download" in line:
            download = float(re.findall(r"[\d.]+", line)[0])

        elif "Upload" in line:
            upload = float(re.findall(r"[\d.]+", line)[0])

    return download, upload, ping


import subprocess
import re

def get_ping():

    result = subprocess.run(
        ["ping", "8.8.8.8", "-n", "4"],
        capture_output=True,
        text=True
    )

    output = result.stdout

    average = 0.0
    packet_loss = 0

    for line in output.splitlines():

        if "Average =" in line:
            match = re.search(r"Average\s*=\s*(\d+)", line)
            if match:
                average = float(match.group(1))

        if "Lost =" in line:
            match = re.search(r"Lost\s*=\s*(\d+)", line)
            if match:
                packet_loss = int(match.group(1))

    return average, packet_loss

if __name__ == "__main__":
    avg, loss = get_ping()
    print("Average Ping:", avg)
    print("Packet Loss:", loss)

    
import netifaces
import nmap

def get_connected_devices():

    try:
        scanner = nmap.PortScanner()

        # Get default gateway
        gateways = netifaces.gateways()

        if 'default' not in gateways:
            print("No default gateway found.")
            return 0

        gateway = gateways['default'][netifaces.AF_INET][0]

        # Create subnet automatically
        subnet = ".".join(gateway.split(".")[:3]) + ".0/24"

        print("=" * 60)
        print("NETWORK DEVICE SCANNER")
        print("=" * 60)
        print("Gateway :", gateway)
        print("Subnet  :", subnet)
        print("Scanning network...")

        scanner.scan(
            hosts=subnet,
            arguments="-sn"
        )

        devices = scanner.all_hosts()

        print("\nConnected Devices")
        print("-" * 60)

        print("{:<18} {:<12} {:<25}".format(
            "IP Address",
            "Status",
            "Hostname"
        ))

        print("-" * 60)

        for host in devices:

            hostname = scanner[host].hostname()

            if hostname == "":
                hostname = "Unknown"

            print("{:<18} {:<12} {:<25}".format(
                host,
                scanner[host].state(),
                hostname
            ))

        print("-" * 60)
        print("Total Connected Devices :", len(devices))
        print("=" * 60)

        return len(devices)

    except Exception as e:

        print("=" * 60)
        print("DEVICE SCAN FAILED")
        print("=" * 60)
        print(e)
        print("=" * 60)

        return 0
    
from pythonping import ping

def get_jitter():

    rtts = []

    for _ in range(5):
        response = ping("8.8.8.8", count=1)
        rtts.append(response.rtt_avg_ms)

    jitter = max(rtts) - min(rtts)

    return round(jitter, 2)

def calculate_health(download, upload, ping, packet_loss,
                     jitter, bandwidth, devices):

    score = 100

    if download < 20:
        score -= 20

    if upload < 10:
        score -= 15

    if ping > 100:
        score -= 20
    elif ping > 50:
        score -= 10

    if packet_loss > 0:
        score -= packet_loss * 5

    if jitter > 30:
        score -= 10

    if bandwidth < 5:
        score -= 10

    if devices > 20:
        score -= 10

    return max(0, min(100, int(score)))

def predict_status(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Good"

    elif score >= 50:
        return "Fair"

    else:
        return "Critical"