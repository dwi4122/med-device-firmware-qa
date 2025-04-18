import shutil
from config import BACKUP_FIRMWARE_PATH, DEVICE_FIRMWARE_PATH
from influx_logger import log_event

def rollback():
    try:
        shutil.copyfile(BACKUP_FIRMWARE_PATH, DEVICE_FIRMWARE_PATH)
        log_event("firmware_rollback", {"status": "rolled_back"})
        print("Firmware rollback completed.")
    except Exception as e:
        log_event("firmware_rollback", {"status": "failed", "error": str(e)})
        raise

if __name__ == "__main__":
    rollback()
