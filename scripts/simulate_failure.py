"""Simulate partial firmware update to mimic power failure."""

import os
from config import NEW_FIRMWARE_PATH, DEVICE_FIRMWARE_PATH


def simulate_partial_copy():
    """Copy only part of the firmware to simulate a failed update."""
    with open(NEW_FIRMWARE_PATH, 'rb') as src, open(DEVICE_FIRMWARE_PATH, 'wb') as dst:
        dst.write(src.read(1024 * 10))  # Simulate 10KB write
    print("Partial firmware update simulated (power failure).")


if __name__ == "__main__":
    simulate_partial_copy()
