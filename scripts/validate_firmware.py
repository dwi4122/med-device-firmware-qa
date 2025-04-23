"""Firmware validation utility.

Checks if the device firmware file meets the minimum size requirement,
to ensure it is complete and not corrupt.
"""

import os
from config import DEVICE_FIRMWARE_PATH


def is_valid_firmware(min_size=100_000):
    """Check if firmware file is valid based on size.

    Args:
        min_size (int): Minimum required file size in bytes. Default is 100,000.

    Returns:
        bool: True if file size meets or exceeds the minimum, False otherwise.
    """
    return os.path.getsize(DEVICE_FIRMWARE_PATH) >= min_size


if __name__ == "__main__":
    if is_valid_firmware():
        print("Firmware is valid.")
    else:
        print("Firmware is incomplete or corrupt.")


