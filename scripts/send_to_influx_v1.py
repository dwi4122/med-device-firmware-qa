import xml.etree.ElementTree as ET
import requests

INFLUX_URL = "http://localhost:8086/write?db=cpap_tests"

def parse_robot_results(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    statistics = root.find("statistics")
    total, passed, failed = 0, 0, 0

    if statistics is not None:
        total_stat = statistics.find("total/stat")
        if total_stat is not None:
            passed = int(total_stat.attrib.get("pass", 0))
            failed = int(total_stat.attrib.get("fail", 0))
            total = passed + failed

    elapsed_time = root.attrib.get("elapsedtime", 0)
    return total, passed, failed, int(elapsed_time)

def send_to_influx(total, passed, failed, elapsed):
    data = f"robot_tests total={total},passed={passed},failed={failed},elapsed={elapsed}"
    response = requests.post(INFLUX_URL, data=data)
    if response.status_code != 204:
        print("❌ Failed to send metrics:", response.status_code, response.text)
    else:
        print("✅ Metrics sent to InfluxDB.")

if __name__ == "__main__":
    total, passed, failed, elapsed = parse_robot_results("output.xml")
    print(f"Parsed: total={total}, passed={passed}, failed={failed}, elapsed={elapsed}")
    send_to_influx(total, passed, failed, elapsed)
