import sqlite3

conn = sqlite3.connect("C:/Users/Vishwa/Desktop/AI_NETWORK_MONITOR/data/network.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS network_config (
    id INTEGER PRIMARY KEY,
    network TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
INSERT OR REPLACE INTO network_config (id, network)
VALUES (1, '192.168.1.0/24')
""")

conn.commit()
conn.close()

print("network_config table created successfully!")