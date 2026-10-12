# AI-Based Network Health Monitoring and Predictive Alerting System

A Python-based network monitoring project that collects system and network performance metrics, stores them in SQLite, calculates a network health score, predicts possible network issues, and presents monitoring results through a Node-RED Dashboard. Telegram notifications can be used to alert administrators about important network events.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Run the Project](#run-the-project)
- [Dashboard](#dashboard)
- [Database](#database)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)
- [Future Enhancements](#future-enhancements)

## Overview

Traditional monitoring systems often report problems after performance has already degraded. This project aims to support proactive monitoring by collecting performance metrics continuously and using trend/risk logic to estimate the current and potential condition of a network.

The system monitors CPU, RAM, disk, internet speed, ping, packet loss, bandwidth usage, and connected devices. It stores collected metrics in an SQLite database and displays health information and prediction results through Node-RED Dashboard 2.0.

## Features

- **Real-time system monitoring:** CPU, RAM, and disk usage.
- **Network performance monitoring:** Ping, packet loss, jitter, internet download/upload speed, and bandwidth.
- **Connected-device monitoring:** Detects devices on a configured local network, subject to network permissions and scanning tools.
- **Network health score:** Calculates a score representing current network condition.
- **Predictive status:** Uses the project's risk/prediction logic to classify network conditions, including:
  - Stable Network
  - Latency Increasing
  - Congestion Expected
  - Critical Network Warning
- **SQLite storage:** Maintains historical monitoring records.
- **Node-RED dashboard:** Presents metrics, health information, and prediction results.
- **Telegram notifications:** The intended integration can send alerts, suppress duplicates/cool down repeated alerts, and report recovery events.
- **Configurable network range:** Network settings can be managed through the project's configuration/dashboard workflow.

> **Note:** The exact availability of features depends on the code and Node-RED flow included in the repository and on the local configuration. Verify Telegram credentials and the dashboard flow before describing a feature as enabled in a particular deployment.

## System Architecture

```text
Local Computer / Network
          |
          v
Python Monitoring Scripts
  - CPU, RAM, disk
  - Ping, packet loss, jitter
  - Speed and bandwidth
  - Connected devices
          |
          v
Health / Risk / Prediction Logic
          |
          v
SQLite Database (network.db)
          |
          v
Node-RED SQLite Queries and Flow
          |
          v
Node-RED Dashboard 2.0
  - System and network metrics
  - Network health score
  - AI/risk prediction
  - Connected devices

Optional alert path:
Monitoring / prediction logic -> Telegram Bot -> Notifications
```

## Technologies Used

- **Python 3**
- **SQLite**
- **Node-RED**
- **Node-RED Dashboard 2.0**
- **psutil** — system and network statistics
- **speedtest-cli** — internet speed tests
- **python-nmap / Nmap** — local device scanning, if used by the selected script
- **joblib** — loading a saved model, if required by the project
- **scikit-learn** — required if the saved model depends on it
- Python standard-library modules such as `sqlite3`, `subprocess`, `datetime`, and `time`
- **Telegram Bot API** — for notification functionality, if configured

## Project Structure

The following is an example layout. Keep the actual filenames and directories in your repository if they differ.

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
├── requirements.txt
└── README.md
```

Do not commit generated database files, model files, or Node-RED flow exports unless you intend to distribute them. If the project needs a model or flow to run, include the required artifact or document how to create/import it.

## Prerequisites

1. Windows, Linux, or macOS with Python installed.
2. Node.js and Node-RED installed.
3. Node-RED Dashboard 2.0 and the required SQLite node installed in Node-RED.
4. Internet access for speed tests and external ping targets.
5. Nmap installed and available on `PATH` if device scanning uses it.
6. The project files, including any required trained model file and Node-RED flow export.

Check the installations:

```powershell
python --version
python -m pip --version
node --version
npm --version
node-red --version
```

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_FOLDER>
```

Replace the placeholders with your actual GitHub repository URL and folder name.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the environment's Python directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### 3. Install Python dependencies

If the repository includes `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

If no requirements file exists yet, install the packages actually imported by the project. A starting list may be:

```bash
python -m pip install psutil speedtest-cli joblib scikit-learn python-nmap netifaces
```

Some packages may not be required by every script. The `sqlite3`, `datetime`, `subprocess`, and `time` modules are included with Python and do not need separate installation. If a package fails to install, check the Python version supported by that package; using a stable Python release supported by all project dependencies may be easier than using a very new release.

### 4. Install Node-RED components

Install Node-RED using its official installation instructions: https://nodered.org/docs/getting-started/

In the Node-RED editor, use **Menu → Manage palette → Install** to install the nodes required by your flow, including:

- Node-RED Dashboard 2.0 (`@flowfuse/node-red-dashboard`)
- The SQLite node package used by the exported flow

The exact SQLite package must match the node type referenced in your flow.

### 5. Import the Node-RED flow

1. Start Node-RED.
2. Open `http://localhost:1880`.
3. Choose **Menu → Import**.
4. Import the project's exported flow JSON, if provided.
5. Confirm that the SQLite nodes point to the correct local database file.
6. Click **Deploy**.

Do not replace the flow with a different one unless necessary; first ensure its database configuration and SQL queries match the local database schema.

## Configuration

### Database path

Make sure the Python scripts and Node-RED SQLite nodes use the **same database file**. A relative path such as `data/network.db` depends on the current working directory; an absolute path can be machine-specific.

For portability, configure the database path relative to the project directory or through an environment variable instead of hard-coding another user's Windows path.

### Model path

If the monitoring script loads `model/network_model.pkl`, confirm that the file exists at the configured location. Do not commit a model unless you have permission to share it and it contains no sensitive data.

### Network range

Set the monitored local network range to match your own network. Device discovery may require Nmap and suitable local network permissions. Only scan networks you own or are authorized to monitor.

### Telegram Bot (optional)

If Telegram notifications are enabled, configure the bot token and destination chat ID through environment variables or a local configuration file that is excluded from Git. Never publish bot tokens or private chat identifiers.

## Run the Project

Open a terminal in the repository root.

### 1. Start the monitoring script

For the script layout shown above:

```powershell
python scripts\monitor.py
```

If `monitor.py` is located in the root directory instead, run:

```powershell
python monitor.py
```

Leave the monitoring process running so it can continue collecting data. If device monitoring is a separate process in your version, open a second terminal and run:

```powershell
python scripts\device_monitor.py
```

Only run scripts that exist in your checked-out project and are intended to run independently.

### 2. Start Node-RED

In a separate terminal:

```powershell
node-red
```

If PowerShell reports that `node-red.ps1` cannot run because script execution is disabled, you can either run the available command shim:

```powershell
node-red.cmd
```

or, if necessary, allow locally installed scripts for the current user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Only change the execution policy if you understand and are permitted to change this setting on your computer.

### 3. Open the dashboard

Open the dashboard URL configured in your Node-RED flow. For many Dashboard 2.0 installations, the path is configured by the flow; use the URL shown by the dashboard nodes. Example:

```text
http://localhost:1880/dashboard
```

Your flow may use a different path, such as `/dashboardnetwork`. Use the path configured in your own flow.

## Dashboard

The dashboard is intended to show:

- CPU, RAM, and disk usage
- Ping, packet loss, and jitter
- Download/upload speed and bandwidth
- Connected devices
- Network health score and health label
- Predicted network status and related risk information

The dashboard can only update when new metrics are written to the database **and** Node-RED successfully queries the same database and passes the results to the widgets.

## Database

The primary monitoring table is named `network_metrics`. The table schema can vary by project version. Check the schema before running SQL queries:

```powershell
python -c "import sqlite3; c=sqlite3.connect('data/network.db'); print(c.execute('PRAGMA table_info(network_metrics)').fetchall()); c.close()"
```

Check whether records are being inserted:

```powershell
python -c "import sqlite3; c=sqlite3.connect('data/network.db'); print('Rows:', c.execute('SELECT COUNT(*) FROM network_metrics').fetchone()[0]); print('Latest ID:', c.execute('SELECT MAX(id) FROM network_metrics').fetchone()[0]); c.close()"
```

Run these commands from the project root if your database is at `data/network.db`. If the database is elsewhere, replace the path with the actual database path.

## Troubleshooting

### Dashboard values are blank or stale

1. Confirm that the Python monitoring script is still running.
2. Check whether the row count or latest record ID in `network_metrics` increases over time.
3. Verify that Node-RED and Python use the exact same database file.
4. Check the Node-RED Debug sidebar for SQLite errors.
5. Verify that the SQL query uses columns that actually exist in the local table.
6. Deploy the flow and refresh the dashboard after correcting any configuration errors.

### `SQLITE_ERROR: no such column`

This means a SQL query refers to a column that does not exist in the database selected by that SQLite node.

1. Run the `PRAGMA table_info(network_metrics)` command above against the exact database file selected in Node-RED.
2. Compare the returned column names with every column in the node's SQL query.
3. Remove or correct references to missing columns, or intentionally migrate the database schema if that column is genuinely required.
4. Repeat the schema check for the exact database path shown in the Node-RED SQLite node.

Do not assume that two database files with the same name have the same schema. A project folder copied from another computer may contain multiple `network.db` files with different columns.

### Python script runs but the dashboard does not update

- Confirm the database row count/latest ID changes while the monitoring script runs.
- If the database updates but Node-RED Debug shows SQLite errors, resolve the query/schema mismatch first.
- Confirm that the SQLite polling/query node is triggered repeatedly by the flow.
- Confirm that the query result is connected to the correct dashboard widget and that the widget expects the received data format.

### `node-red.ps1 cannot be loaded`

Try `node-red.cmd` in PowerShell. If that command is unavailable, review the Node-RED installation and PowerShell execution policy.

### Missing Python module

Install the missing package in the same Python environment used to run the project:

```powershell
python -m pip install <package-name>
```

### Saved model file not found

Verify the configured model path and ensure `network_model.pkl` exists. Update machine-specific paths to a portable project-relative path.

## Security Notes

- Do not commit `.env` files, Telegram bot tokens, passwords, private IP inventories, or other secrets.
- Use `.gitignore` for virtual environments, caches, logs, local databases, and private configuration files.
- Scan only networks you own or have explicit permission to monitor.
- Avoid exposing the Node-RED editor or dashboard publicly without appropriate authentication and network controls.
- Check the license and redistribution permissions for datasets, models, and third-party components before publishing them.

## Future Enhancements

- Improve prediction accuracy using historical network data and advanced machine-learning methods.
- Add cloud database storage and centralized monitoring.
- Add advanced anomaly detection.
- Introduce Quality of Service (QoS) analysis.
- Classify network traffic by application or protocol.
- Add automated recovery actions for selected network failures.
- Extend security monitoring to flag suspicious connections and abnormal traffic.

## Acknowledgements

This project was developed as an AI-based network health monitoring and predictive alerting system. The internship report identifies the National Institute of Technology, Warangal, and the NIT Warangal–SIEMENS Centre of Excellence for Digital Manufacturing and Automation as the internship context.

---

**Maintainer:** Add your name or GitHub username here  
**Project:** AI-Based Network Health Monitoring and Predictive Alerting System
