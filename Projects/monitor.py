import psutil
import csv
import os
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "data/server_health.csv")
LOG_FILE = os.path.join(BASE_DIR, "logs/monitor.log")

def log_message(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} - {message}\n")

def get_gpu_usage():
    try:
        output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
            stderr=subprocess.DEVNULL
        )
        return output.decode().strip() + "%"
    except:
        return "N/A"

def create_csv_if_not_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timestamp",
                "CPU_Usage(%)",
                "RAM_Usage(%)",
                "Disk_Usage(%)",
                "GPU_Usage(%)"
            ])

def collect_metrics():
    return [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        psutil.cpu_percent(interval=1),
        psutil.virtual_memory().percent,
        psutil.disk_usage("/").percent,
        get_gpu_usage()
    ]

def write_metrics(data):
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

def main():
    create_csv_if_not_exists()
    metrics = collect_metrics()
    write_metrics(metrics)
    log_message("Metrics collected successfully")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_message(f"ERROR: {e}")
