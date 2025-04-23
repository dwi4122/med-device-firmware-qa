*** Settings ***
Library    OperatingSystem
Library    Process
Library    Collections


*** Variables ***
${APNEA_THRESHOLD}    10.0

*** Test Cases ***
Valid Firmware Update
    [Documentation]    Test complete firmware update process with validation
    Run Process    python3    scripts/firmware_updater.py
    Run Process    python3    scripts/validate_firmware.py
    Run Process    python3    scripts/checksum_validator.py

