"""Parse Robot Framework results and send metrics to InfluxDB and Grafana."""

import xml.etree.ElementTree as ET
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class ResultParser:
    """Handles parsing and sending test results to monitoring systems."""
    
    def __init__(self, influx_host: str = 'localhost', influx_port: int = 8086,
                 influx_db: str = 'cpap_tests'):
        """Initialize with InfluxDB connection details."""
        self.influx_url = f"http://{influx_host}:{influx_port}/write?db={influx_db}"
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def parse_robot_results(self, xml_file: str) -> Tuple[Optional[Dict], Optional[List[str]]]:
        """Extract test statistics from Robot Framework output.xml.

        Args:
            xml_file: Path to the Robot Framework output XML.

        Returns:
            tuple: (metrics dict, list of failed test names) or (None, None) on error
        """
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            stats = {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'elapsed': int(root.attrib.get('elapsedtime', 0)) // 1000
            }

            total_stat = root.find('statistics/total/stat')
            if total_stat is not None:
                stats['passed'] = int(total_stat.attrib.get('pass', 0))
                stats['failed'] = int(total_stat.attrib.get('fail', 0))
                stats['total'] = stats['passed'] + stats['failed']

            failed_tests = [
                test.attrib['name']
                for test in root.findall('.//test/status[@status="FAIL"]/..')
            ]

            return stats, failed_tests

        except (ET.ParseError, FileNotFoundError) as e:
            print(f'Error parsing {xml_file}: {str(e)}')
            return None, None

    def send_to_influx(self, metrics: Dict, failed_tests: Optional[List[str]] = None) -> bool:
        """Send test metrics to InfluxDB with retry logic.

        Args:
            metrics: Parsed test metrics.
            failed_tests: Optional list of failed test names.

        Returns:
            bool: True on success, False otherwise.
        """
        if not metrics:
            return False

        timestamp = int(time.time() * 1e9)  # nanoseconds
        base_data = (
            f'robot_tests,device_type=CPAP '
            f'total={metrics["total"]},passed={metrics["passed"]},'
            f'failed={metrics["failed"]},duration={metrics["elapsed"]} '
            f'{timestamp}'
        )

        if failed_tests:
            tests_str = ','.join(failed_tests).replace(' ', '\\ ')
            base_data += (
                f'\nrobot_tests,failure_detail tests="{tests_str}" {timestamp}'
            )

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.influx_url,
                    data=base_data,
                    timeout=5
                )
                if response.status_code == 204:
                    print(f'✅ Metrics sent to InfluxDB at {datetime.now()}')
                    return True
                print(f'⚠️ Attempt {attempt + 1}: InfluxDB error {response.status_code}')
            except requests.exceptions.RequestException as e:
                print(f'⚠️ Attempt {attempt + 1}: Connection failed - {str(e)}')

            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay)

        print('❌ All retries failed')
        return False


if __name__ == '__main__':
    parser = ResultParser()
    metrics, failed_tests = parser.parse_robot_results('output.xml')

    if metrics:
        print(f"""\nTest Results:
        Total: {metrics['total']}
        Passed: {metrics['passed']}
        Failed: {metrics['failed']}
        Duration: {metrics['elapsed']}s
        Failed Tests: {failed_tests or 'None'}""")

        parser.send_to_influx(metrics, failed_tests)
    else:
        print('No valid metrics to send.')