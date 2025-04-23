"""Pressure control validation for CPAP firmware.

Provides Robot Framework keywords to test pressure accuracy
in compliance with ISO 80601-2-70.
"""

from robot.api.deco import keyword
from influx_logger import AuditLogger

_logger = AuditLogger()

# ISO 80601-2-70 specifies ±0.5 cmH2O tolerance for pressure delivery
TOLERANCE = 0.5


@keyword("Validate Pressure")
def validate_pressure(measured_pressure, target_pressure=12.0):
    """Validate pressure reading is within ISO-compliant tolerance.

    Args:
        measured_pressure: Measured value (str or float).
        target_pressure: Target value in cmH2O (default: 12.0).

    Returns:
        bool: True if within range, False if outside tolerance.

    Raises:
        ValueError: If inputs cannot be converted to float.
    """
    try:
        pressure = float(measured_pressure)
        target = float(target_pressure)

        within_tolerance = abs(pressure - target) <= TOLERANCE

        _logger.log_event("pressure_test", {
            "target": target,
            "measured": pressure,
            "result": "passed" if within_tolerance else "failed"
        })

        print(f"Pressure validation: target={target}, measured={pressure}, result={within_tolerance}")
        return within_tolerance

    except (ValueError, TypeError):
        _logger.log_event("pressure_test", {
            "target": target_pressure,
            "measured": measured_pressure,
            "result": "error"
        })
        print("Invalid input for pressure validation.")
        raise


# Required by Robot Framework to register keywords
ROBOT_LIBRARY_SCOPE = "GLOBAL"
