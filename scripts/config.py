# scripts/config.py

from pathlib import Path

BASE_DIR = Path("/home/pi/cpap-firmware-simulator")
FIRMWARE_DIR = BASE_DIR / "firmware"
DEVICE_FIRMWARE_PATH = BASE_DIR / "firmware" / "installed_firmware.bin"
NEW_FIRMWARE_PATH = FIRMWARE_DIR / "new_firmware.bin"
BACKUP_FIRMWARE_PATH = FIRMWARE_DIR / "firmware_backup.bin"
