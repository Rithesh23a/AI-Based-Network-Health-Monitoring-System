# AI-Based Network Health Monitoring and Predictive Alerting System

## 1. Introduction

The AI-Based Network Health Monitoring and Predictive Alerting System continuously monitors computer system and network performance. It collects metrics such as CPU usage, RAM usage, disk usage, internet speed, ping, packet loss, jitter, bandwidth usage, and connected devices. The collected data is stored in an SQLite database and analyzed to calculate network health scores and predict potential network issues. Node-RED Dashboard 2.0 provides a graphical interface for monitoring network performance and health.

## 2. Problem Statement

Traditional network monitoring systems primarily identify issues after network performance has degraded. Manual monitoring can delay the detection and resolution of network problems. Therefore, a system is needed to continuously monitor performance metrics, assess network health, predict potential network issues, and provide timely alerts through a centralized dashboard.

## 3. Dataset Used

The project uses continuously collected system and network performance metrics rather than relying exclusively on a predefined static dataset.

The collected data includes:
- CPU, RAM, and disk utilization.
- Internet download and upload speeds.
- Ping, packet loss, and jitter.
- Network bandwidth usage.
- Number of connected devices.
- Network health score and predicted status.

The data is stored in an SQLite database, primarily in the `network_metrics` table. A trained machine-learning model, `network_model.pkl`, is used if available in the configured project setup.

## 4. Methodology

1. **Metric Collection:** Python scripts collect system and network performance information using monitoring libraries and utilities.
2. **Data Storage:** Collected metrics are stored in an SQLite database for historical tracking.
3. **Health Assessment:** The system calculates a network health score using monitored performance metrics.
4. **Prediction:** The configured prediction logic or trained model estimates network conditions and identifies potential performance risks.
5. **Device Monitoring:** A separate script can monitor devices connected to the local network.
6. **Dashboard Integration:** Node-RED queries the SQLite database and processes the results for visualization.
7. **Alerting:** Network status and potential issues are displayed on the dashboard, with optional Telegram notifications when configured.

## 5. Evaluation Strategy

The system can be evaluated using the following criteria:

- **Metric Accuracy:** Compare reported metrics with operating-system monitoring tools.
- **Data Collection Reliability:** Verify that new records are continuously inserted into SQLite.
- **Dashboard Update Frequency:** Check whether dashboard values refresh as new metrics arrive.
- **Prediction Performance:** Evaluate the model using accuracy, precision, recall, F1-score, and a confusion matrix when labeled test data is available.
- **Alert Effectiveness:** Verify that warnings are generated for relevant network conditions.
- **System Reliability:** Check whether monitoring operates continuously without unexpected interruptions.

*Numerical evaluation results should be included only after conducting the corresponding tests.*

## 6. Dashboard

The project uses Node-RED Dashboard 2.0 to visualize network performance and health.

Dashboard components include:

- **System Health:** CPU, RAM, and disk utilization.
- **Network Performance:** Ping, packet loss, jitter, download speed, and upload speed.
- **Bandwidth Information:** Network traffic and bandwidth usage.
- **Network Health Card:** Current health score and health status.
- **AI Prediction:** Predicted network condition, confidence, and risk information when provided by the configured model.
- **Connected Devices:** Information about devices detected on the monitored network.

The dashboard retrieves data through Node-RED flows and SQLite queries. Live updates require successful database access, valid SQL queries, and repeated execution of the monitoring flow.

## 7. Project Structure

```text
AI_NETWORK_MONITOR/
├── scripts/
│   ├── monitor.py
│   ├── device_monitor.py
│   └── create_network_config.py
├── utils.py
├── ai_model.py
├── model/
│   └── network_model.pkl
├── data/
│   └── network.db
├── flows/
│   └── flows.json
└── README.md
```

*This is a representative structure. Actual filenames and locations may differ in the repository.*

## 8. How to Run the Dashboard

### Step 1: Install Dependencies

Install Python, Node.js, and Node-RED. Install the Python packages required by the project:

```bash
python -m pip install psutil speedtest-cli joblib scikit-learn netifaces
```

Install any additional packages imported by the project and the required Node-RED Dashboard 2.0 and SQLite nodes.

### Step 2: Run the Monitoring Script

Open a terminal in the project root directory and run:

```powershell
python scripts\monitor.py
```

Keep the script running so that new metrics can be collected and stored.

If device monitoring is implemented as a separate process, open another terminal and run:

```powershell
python scripts\device_monitor.py
```

### Step 3: Start Node-RED

Open another terminal and run:

```powershell
node-red
```

If PowerShell blocks the command, try:

```powershell
node-red.cmd
```

### Step 4: Configure and Deploy the Flow

1. Open `http://localhost:1880` in your browser.
2. Import the project's Node-RED flow JSON if it is not already loaded.
3. Ensure the SQLite nodes reference the same database file used by the Python monitoring script.
4. Verify that the SQL queries use columns present in the selected database.
5. Click **Deploy**.

### Step 5: Open the Dashboard

Open the dashboard URL configured in the Node-RED flow. For example:

```text
http://localhost:1880/dashboardnetwork
```

Use the actual dashboard path configured in your project if it differs.

Keep the Python monitoring script and Node-RED running. The dashboard updates when new metrics are written to the database and the Node-RED flow successfully retrieves and forwards them to the dashboard widgets.
