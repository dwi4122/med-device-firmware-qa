"""Parse Robot Framework results and send metrics to InfluxDB."""

import xml.etree.ElementTree as ET
import requests
import time
from datetime import datetime

# Configuration
INFLUX_URL = "http://localhost:8086/write?db=cpap_tests"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


def parse_robot_results(xml_file):
    """Extract test statistics from Robot Framework output.xml.

    Args:
        xml_file (str): Path to the Robot Framework output XML.

    Returns:
        tuple: (metrics dict, list of failed test names)
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        stats = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "elapsed": int(root.attrib.get("elapsedtime", 0)) // 1000
        }

        total_stat = root.find("statistics/total/stat")
        if total_stat is not None:
            stats["passed"] = int(total_stat.attrib.get("pass", 0))
            stats["failed"] = int(total_stat.attrib.get("fail", 0))
            stats["total"] = stats["passed"] + stats["failed"]

        failed_tests = [
            test.attrib["name"]
            for test in root.findall(".//test/status[@status='FAIL']/..")
        ]

        return stats, failed_tests

    except (ET.ParseError, FileNotFoundError) as e:
        print(f"⚠️ Error parsing {xml_file}: {str(e)}")
        return None, None


def send_to_influx(metrics, failed_tests=None):
    """Sends test metrics to InfluxDB with retry logic.

    Args:
        metrics (dict): Parsed test metrics.
        failed_tests (list): Optional list of failed test names.

    Returns:
        bool: True on success, False otherwise.
    """
    if not metrics:
        return False

    timestamp = int(time.time() * 1e9)  # nanoseconds
    base_data = (
        f"robot_tests,device_type=CPAP "
        f"total={metrics['total']},passed={metrics['passed']},"
        f"failed={metrics['failed']},duration={metrics['elapsed']} {timestamp}"
    )

    if failed_tests:
        tests_str = ",".join(failed_tests).replace(" ", "\\ ")
        base_data += (
            f"\nrobot_tests,failure_detail tests=\"{tests_str}\" {timestamp}"
        )

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(INFLUX_URL, data=base_data, timeout=5)
            if response.status_code == 204:
                print(f"✅ Metrics sent to InfluxDB at {datetime.now()}")
                return True
            print(f"⚠️ Attempt {attempt + 1}: InfluxDB error {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Attempt {attempt + 1}: Connection failed - {str(e)}")

        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY)

    print("❌ All retries failed")
    return False


if __name__ == "__main__":
    metrics, failed_tests = parse_robot_results("output.xml")

    if metrics:
        print(f"""\nTest Results:
        Total: {metrics['total']}
        Passed: {metrics['passed']}
        Failed: {metrics['failed']}
        Duration: {metrics['elapsed']}s
        Failed Tests: {failed_tests or 'None'}""")

        send_to_influx(metrics, failed_tests)
    else:
        print("No valid metrics to send.")
