*** Settings ***
Library    OperatingSystem
Library    Process
Library    InfluxDBListener    host=localhost    port=8086    database=robot_metrics

*** Test Cases ***
Simulate Update Interruption
    Run Process    python3    scripts/simulate_failure.py
    Run Process    python3    scripts/validate_firmware.py
