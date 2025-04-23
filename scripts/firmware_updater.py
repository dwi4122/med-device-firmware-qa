"""Firmware update functionality with logging and validation.

This module handles the firmware update process for CPAP devices, including
safety checks and logging for regulatory compliance.
"""

import shutil
from typing import NoReturn
from config import NEW_FIRMWARE_PATH, DEVICE_FIRMWARE_PATH
from influx_logger import log_event
from validation import validate_firmware_integrity

def update_firmware() -> None:
    """Perform a firmware update with validation and logging.
    
    Raises:
        RuntimeError: If the update fails or validation checks don't pass
    """
    try:
        # Create backup before updating
        shutil.copyfile(DEVICE_FIRMWARE_PATH, BACKUP_FIRMWARE_PATH)
        
        # Perform the update
        shutil.copyfile(NEW_FIRMWARE_PATH, DEVICE_FIRMWARE_PATH)
        
        # Validate the update
        if not validate_firmware_integrity(DEVICE_FIRMWARE_PATH):
            raise RuntimeError("Firmware validation failed after update")
            
        log_event("firmware_update", {"status": "success"})
        print("Firmware update completed successfully.")
    except Exception as e:
        log_event("firmware_update", {"status": "failed", "error": str(e)})
        raise RuntimeError(f"Firmware update failed: {str(e)}") from e

if __name__ == "__main__":
    update_firmware()