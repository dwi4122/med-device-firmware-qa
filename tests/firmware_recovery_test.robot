*** Settings ***
Library    OperatingSystem
Library    Process

*** Test Cases ***
Rollback After Failed Update
    Run Process    python3    scripts/simulate_failure.py
    Run Process    python3    scripts/validate_firmware.py
    Run Process    python3    scripts/rollback.py
    Run Process    python3    scripts/validate_firmware.py
    Run Process    python3    scripts/checksum_validator.py
