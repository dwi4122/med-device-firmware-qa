import shutil
from config import NEW_FIRMWARE_PATH, DEVICE_FIRMWARE_PATH
from influx_logger import log_event

def update_firmware():
    try:
        shutil.copyfile(NEW_FIRMWARE_PATH, DEVICE_FIRMWARE_PATH)
        log_event("firmware_update", {"status": "success"})
        print("Firmware update completed successfully.")
    except Exception as e:
        log_event("firmware_update", {"status": "failed", "error": str(e)})
        raise

if __name__ == "__main__":
    update_firmware()
