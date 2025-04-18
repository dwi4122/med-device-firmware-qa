import os
from config import DEVICE_FIRMWARE_PATH

def is_valid_firmware(min_size=100_000):
    return os.path.getsize(DEVICE_FIRMWARE_PATH) >= min_size

if __name__ == "__main__":
    if is_valid_firmware():
        print("Firmware is valid.")
    else:
        print("Firmware is incomplete or corrupt.")
