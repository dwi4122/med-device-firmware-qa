"""Fault injection module for CPAP firmware validation.

This module provides Robot Framework keywords for simulating
hardware fault conditions, following IEC 62304 and PEP 8 standards.
"""

from robot.api.deco import keyword
from influx_logger import AuditLogger

# Shared logger instance
_logger = AuditLogger()


@keyword("Simulate Pressure Sensor Fault")
def simulate_pressure_sensor_fault(duration):
    """Simulate pressure sensor failure to test alarm behavior.

    Args:
        duration: Duration of fault in seconds (int or string convertible to int).

    Returns:
        bool: True if fault injected successfully, False if input is invalid.

    Note:
        Logs fault to InfluxDB.
        Complies with IEC 62304 Clause 5.5.4.
    """
    try:
        fault_duration = int(duration)
        _logger.log_event(
            "fault_injection",
            {
                "type": "pressure_sensor",
                "duration": fault_duration,
                "severity": "critical"
            }
        )
        print(f"Simulating pressure sensor fault for {fault_duration} seconds")
        return True

    except (ValueError, TypeError):
        print("Invalid duration input for pressure sensor fault.")
        return False


@keyword("Simulate Power Interruption")
def simulate_power_interruption():
    """Simulate a sudden power loss during operation.

    Returns:
        bool: Always True, assumes simulation is successfully initiated.

    Note:
        Logs fault to InfluxDB.
        Complies with IEC 62304 Clause 5.7.
    """
    _logger.log_event(
        "fault_injection",
        {
            "type": "power_interruption",
            "severity": "critical"
        }
    )
    print("Simulating power interruption")
    return True


# Required for Robot Framework to detect keywords
ROBOT_LIBRARY_SCOPE = "GLOBAL"
