import pandas as pd
import random

rows = []

for i in range(2000):

    download = round(random.uniform(1,100),2)
    upload = round(random.uniform(0.5,50),2)
    ping = round(random.uniform(5,250),2)
    packet_loss = round(random.uniform(0,10),2)
    jitter = round(random.uniform(0,50),2)
    bandwidth = round(random.uniform(1,100),2)
    devices = random.randint(1,30)

    score = 100

    if download < 10:
        score -= 20

    if upload < 5:
        score -= 10

    if ping > 150:
        score -= 20
    elif ping > 80:
        score -= 10

    if packet_loss > 5:
        score -= 20
    elif packet_loss > 1:
        score -= 10

    if jitter > 30:
        score -= 10

    if devices > 20:
        score -= 10

    score = max(0, score)

    if score >= 85:
        prediction = "Excellent"
    elif score >= 60:
        prediction = "Good"
    else:
        prediction = "Warning"

    rows.append([
        download,
        upload,
        ping,
        packet_loss,
        jitter,
        bandwidth,
        devices,
        score,
        prediction
    ])

df = pd.DataFrame(rows, columns=[
    "download_speed",
    "upload_speed",
    "ping",
    "packet_loss",
    "jitter",
    "download_bandwidth",
    "connected_devices",
    "health_score",
    "prediction"
])

df.to_csv("../dataset/network_dataset.csv", index=False)

print("Dataset Created Successfully!")