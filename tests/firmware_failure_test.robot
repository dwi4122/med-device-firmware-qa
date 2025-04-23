*** Settings ***
Library    OperatingSystem
Library    Process


*** Test Cases ***
Simulate Update Interruption
    Run Process    python3    scripts/simulate_failure.py
    Run Process    python3    scripts/validate_firmware.py
