*** Settings ***
Library    OperatingSystem
Library    Process
Library    InfluxDBListener    host=localhost    port=8086    database=robot_metrics

*** Test Cases ***
Valid Firmware Update
    Run Process    python3    scripts/firmware_updater.py
    Run Process    python3    scripts/validate_firmware.py
    Run Process    python3    scripts/checksum_validator.py



