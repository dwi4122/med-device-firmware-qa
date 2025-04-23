"""Configuration for medical device testing framework."""

from pathlib import Path
from dataclasses import dataclass


@dataclass
class DeviceConfig:
    pressure_tolerance: float = 0.5  # cmH2O
    apnea_threshold: float = 10.0    # seconds
    max_firmware_size: int = 10_000_000  # 10MB


# Path configuration
BASE_DIR = Path("/home/pi/cpap-firmware-simulator")
FIRMWARE_DIR = BASE_DIR / "firmware"
TEST_DATA_DIR = BASE_DIR / "test_data"

DEVICE_FIRMWARE_PATH = FIRMWARE_DIR / "installed_firmware.bin"
NEW_FIRMWARE_PATH = FIRMWARE_DIR / "new_firmware.bin"
BACKUP_FIRMWARE_PATH = FIRMWARE_DIR / "firmware_backup.bin"

# Test configuration instance
device_config = DeviceConfig()
