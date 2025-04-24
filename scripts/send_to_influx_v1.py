import xml.etree.ElementTree as ET
import requests
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class ResultSender:
    def __init__(self):
        # Enhanced InfluxDB configuration with auth support
        self.influx_url = (
            f"http://{os.getenv('INFLUXDB_HOST', 'localhost')}:"
            f"{os.getenv('INFLUXDB_PORT', '8086')}/write?"
            f"db={os.getenv('INFLUXDB_DB', 'cpap_tests')}"
            f"&precision=ns"
        )
        
        # Add InfluxDB auth if configured
        self.influx_auth = None
        if os.getenv('INFLUXDB_USER') and os.getenv('INFLUXDB_PASSWORD'):
            self.influx_auth = (
                os.getenv('INFLUXDB_USER'), 
                os.getenv('INFLUXDB_PASSWORD')
            )

        # Grafana configuration with multiple key options
        self.grafana_url = (
            f"{os.getenv('GRAFANA_URL', 'http://localhost:3000')}/api/annotations"
        )
        self.headers = {
            "Content-Type": "application/json"
        }
        
        # Check for API key in multiple possible environment variables
        grafana_api_key = (
            os.getenv('GRAFANA_API_KEY') or 
            os.getenv('GRAFANA_TOKEN') or
            os.getenv('GRAFANA_ANNOTATION_KEY')
        )
        if grafana_api_key:
            self.headers["Authorization"] = f"Bearer {grafana_api_key}"

        self.timeout = int(os.getenv('REQUEST_TIMEOUT', '5'))

    def parse_results(
        self, xml_file: str
    ) -> Tuple[Optional[Dict], Optional[List[str]]]:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Enhanced duration handling with debugging
            elapsed_time_str = root.get("elapsedtime", "0")
            try:
                elapsed_ms = float(elapsed_time_str)
                # Convert to seconds with 3 decimal places
                elapsed_sec = round(elapsed_ms / 1000, 3)
            except (ValueError, TypeError) as e:
                print(f"Error parsing elapsed time '{elapsed_time_str}': {str(e)}")
                elapsed_sec = 0.0

            metrics = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "elapsed": elapsed_sec,  # Now using precise decimal value
                "elapsed_ms": elapsed_ms,  # Also store original ms value
            }

            # Enhanced stats parsing with error handling
            total_stat = root.find("statistics/total/stat")
            if total_stat is not None:
                try:
                    metrics.update({
                        "passed": int(total_stat.get("pass", 0)),
                        "failed": int(total_stat.get("fail", 0)),
                        "total": (
                            int(total_stat.get("pass", 0)) + 
                            int(total_stat.get("fail", 0))
                        ),
                    })
                except (ValueError, AttributeError) as e:
                    print(f"Error parsing test statistics: {str(e)}")

            # Get failed test names with additional context
            failed_tests = []
            for test in root.findall(".//test"):
                status = test.find("status")
                if status is not None and status.get("status") == "FAIL":
                    test_name = test.get("name", "unnamed_test")
                    failed_tests.append(test_name)
                    # Log additional failure context
                    failure_msg = status.text.strip() if status.text else "no message"
                    print(f"Test failed: {test_name} - {failure_msg}")

            # Debug output
            print(f"Parsed metrics: {metrics}")
            print(f"Failed tests: {failed_tests}")

            return metrics, failed_tests

        except (ET.ParseError, FileNotFoundError, AttributeError) as e:
            print(f"XML parsing error: {str(e)}")
            return None, None

    def send_to_influx(self, metrics: Dict) -> bool:
        if not metrics or metrics.get("total", 0) == 0:
            print("No valid metrics to send")
            return False

        timestamp = int(time.time() * 1e9)
        
        # Enhanced InfluxDB line protocol with additional fields
        data = (
            f"robot_tests,device_type=CPAP "
            f"passed={metrics['passed']},failed={metrics['failed']},"
            f"total={metrics['total']},duration={metrics['elapsed']},"
            f"duration_ms={metrics['elapsed_ms']} "
            f"{timestamp}"
        )

        print(f"Sending to InfluxDB: {data}")

        try:
            response = requests.post(
                self.influx_url,
                data=data,
                timeout=self.timeout,
                auth=self.influx_auth
            )
            if response.status_code == 204:
                print("Successfully sent metrics to InfluxDB")
                return True
            print(f"InfluxDB error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"InfluxDB connection error: {str(e)}")

        return False

    def send_to_grafana(self, status: str, failed_tests: List[str] = None) -> bool:
        if "Authorization" not in self.headers:
            print("Grafana API token not found. Set GRAFANA_API_KEY or GRAFANA_TOKEN environment variable")
            return False

        now_ms = int(time.time() * 1000)
        
        # Enhanced annotation with failure details
        annotation_text = f"Test {status} at {datetime.now().isoformat()}"
        if failed_tests:
            annotation_text += f"\nFailed tests: {', '.join(failed_tests[:5])}"  # Show first 5 failures
            if len(failed_tests) > 5:
                annotation_text += f" (+{len(failed_tests) - 5} more)"

        data = {
            "text": annotation_text,
            "tags": ["jenkins", "robotframework", status.lower()],
            "time": now_ms,
        }

        # Add dashboard reference if configured
        dashboard_id = os.getenv("GRAFANA_DASHBOARD_ID")
        if dashboard_id:
            try:
                data["dashboardId"] = int(dashboard_id)
                data["panelId"] = 2  # Default panel ID for annotations
            except ValueError:
                print(f"Invalid GRAFANA_DASHBOARD_ID: {dashboard_id}")

        print(f"Sending to Grafana: {data}")

        try:
            res = requests.post(
                self.grafana_url,
                json=data,
                headers=self.headers,
                timeout=self.timeout
            )
            res.raise_for_status()
            print(f"Successfully created Grafana annotation (ID: {res.json().get('id', 'unknown')})")
            return True
        except requests.exceptions.HTTPError as e:
            print(f"Grafana error {res.status_code}: {res.text}")
        except requests.exceptions.RequestException as e:
            print(f"Grafana connection error: {e}")

        return False


if __name__ == "__main__":
    print("Starting CPAP test results processing")
    
    sender = ResultSender()
    
    # Allow custom XML file path but default to output.xml
    xml_file = os.getenv('TEST_RESULTS_XML', 'output.xml')
    print(f"Processing test results from: {xml_file}")
    
    metrics, failed_tests = sender.parse_results(xml_file)

    if metrics:
        print(f"\nTest Results Summary:")
        print(f"Passed: {metrics['passed']}")
        print(f"Failed: {metrics['failed']}")
        print(f"Total: {metrics['total']}")
        print(f"Duration: {metrics['elapsed']:.3f} seconds")
        
        # Send to InfluxDB
        print("\nSending metrics to InfluxDB...")
        if sender.send_to_influx(metrics):
            print("InfluxDB update successful")
        else:
            print("Warning: Failed to update InfluxDB")

        # Determine status and send to Grafana
        status = "SUCCESS" if metrics["failed"] == 0 else "FAILURE"
        print(f"\nSending {status} status to Grafana...")
        if sender.send_to_grafana(status, failed_tests if status == "FAILURE" else None):
            print("Grafana update successful")
        else:
            print("Warning: Failed to update Grafana")
    else:
        print("Error: No valid test results to process")

    print("\nProcessing complete")