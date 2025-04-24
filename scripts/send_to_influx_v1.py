import xml.etree.ElementTree as ET
import requests
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()


class ResultSender:
    def __init__(self):
        self.influx_url = (
            f"http://{os.getenv('INFLUXDB_HOST', 'localhost')}:"
            f"{os.getenv('INFLUXDB_PORT', '8086')}/write?"
            f"db={os.getenv('INFLUXDB_DB', 'cpap_tests')}"
            f"&precision=ns"
        )
        self.grafana_url = (
            f"{os.getenv('GRAFANA_URL', 'http://localhost:3000')}/api/annotations"
        )
        self.headers = {
            "Authorization": f"Bearer {os.getenv('GRAFANA_API_KEY')}",
            "Content-Type": "application/json"
        }
        self.timeout = 5

    def parse_results(self, xml_file: str) -> Tuple[Optional[Dict], Optional[List[str]]]:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            metrics = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "elapsed": int(float(root.get("elapsedtime", 0)) // 1000)
            }

            total_stat = root.find("statistics/total/stat")
            if total_stat is not None:
                metrics.update({
                    "passed": int(total_stat.get("pass", 0)),
                    "failed": int(total_stat.get("fail", 0)),
                    "total": int(total_stat.get("pass", 0)) +
                             int(total_stat.get("fail", 0))
                })

            failed_tests = [
                test.get("name")
                for test in root.findall(".//test")
                if test.find("status").get("status") == "FAIL"
            ]

            return metrics, failed_tests

        except (ET.ParseError, FileNotFoundError, AttributeError) as e:
            print(f"XML parsing error: {str(e)}")
            return None, None

    def send_to_influx(self, metrics: Dict) -> bool:
        if not metrics or metrics.get("total", 0) == 0:
            print("No valid metrics to send")
            return False

        timestamp = int(time.time() * 1e9)
        data = (
            f"robot_tests,device_type=CPAP "
            f"passed={metrics['passed']},failed={metrics['failed']},"
            f"total={metrics['total']},duration={metrics['elapsed']} "
            f"{timestamp}"
        )

        try:
            response = requests.post(
                self.influx_url,
                data=data,
                timeout=self.timeout
            )
            if response.status_code == 204:
                return True
            print(f"InfluxDB error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"InfluxDB connection error: {str(e)}")

        return False

    def send_to_grafana(self, status: str) -> bool:
        if not os.getenv("GRAFANA_API_KEY"):
            print("Grafana API token not found. Set GRAFANA_API_KEY in .env")
            return False

        now_ms = int(time.time() * 1000)
        data = {
            "text": f"Test {status} at {datetime.now().isoformat()}",
            "tags": ["jenkins", "robotframework"],
            "time": now_ms
        }

        dashboard_id = os.getenv("GRAFANA_DASHBOARD_ID")
        if dashboard_id:
            data["dashboardId"] = int(dashboard_id)

        try:
            res = requests.post(
                self.grafana_url,
                json=data,
                headers=self.headers,
                timeout=self.timeout
            )
            res.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            print(f"Grafana error {res.status_code}: {res.text}")
        except requests.exceptions.RequestException as e:
            print(f"Grafana connection error: {e}")

        return False


if __name__ == "__main__":
    if not os.path.exists(".env"):
        print("Missing .env configuration file")
        exit(1)

    sender = ResultSender()
    metrics, failed_tests = sender.parse_results("output.xml")

    if metrics:
        print(f"Passed: {metrics['passed']}, Failed: {metrics['failed']}")

        if sender.send_to_influx(metrics):
            print("Successfully sent to InfluxDB")
        else:
            print("Failed to send to InfluxDB")

        status = "SUCCESS" if metrics["failed"] == 0 else "FAILURE"
        if sender.send_to_grafana(status):
            print("Successfully updated Grafana")
        else:
            print("Failed to update Grafana")
    else:
        print("No test results to process")
