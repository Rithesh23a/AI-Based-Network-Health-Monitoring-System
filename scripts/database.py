import sqlite3

conn = sqlite3.connect("../data/network.db")
cursor = conn.cursor()

# Existing table
cursor.execute("""
CREATE TABLE IF NOT EXISTS network_metrics(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    timestamp TEXT,

    cpu REAL,
    ram REAL,
    disk REAL,

    download_speed REAL,
    upload_speed REAL,

    ping REAL,
    packet_loss REAL,

    bytes_sent INTEGER,
    bytes_received INTEGER,

    upload_bandwidth REAL,
    download_bandwidth REAL,

    connected_devices INTEGER,

    health_score INTEGER,

    prediction TEXT
)
""")

# -----------------------------
# NEW TABLE
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS device_metrics(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    timestamp TEXT,

    ip TEXT,

    hostname TEXT,

    status TEXT,

    ping REAL,

    packet_loss REAL,

    health_score INTEGER
)
""")

conn.commit()
conn.close()

print("Database Ready!")