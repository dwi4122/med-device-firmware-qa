# CPAP Firmware Test Simulator
This project simulates and tests firmware updates for CPAP devices using a Raspberry Pi. It is built for IEC 62304-aligned medical device software testing with a focus on automation, rollback, and data traceability.

## Features:

-Simulates real-world firmware update behavior
-Power failure simulation and recovery
-Automated testing using Robot Framework
-Jenkins CI pipeline for regression detection
-File integrity validation using SHA256 checksums
-Real-time metrics dashboard via Grafana

## Setup Instructions:

Clone repo and run pip install -r requirements.txt
Connect Raspberry Pi hardware
Run robot tests/ to start test suite
Launch Jenkins CI 
Grafana for monitoring
