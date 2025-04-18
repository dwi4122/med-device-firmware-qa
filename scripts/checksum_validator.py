import hashlib
from config import NEW_FIRMWARE_PATH, DEVICE_FIRMWARE_PATH

def sha256(path):
    sha = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()

if __name__ == "__main__":
    new_hash = sha256(NEW_FIRMWARE_PATH)
    installed_hash = sha256(DEVICE_FIRMWARE_PATH)
    if new_hash == installed_hash:
        print("Checksum match: Firmware integrity validated.")
    else:
        print("Checksum mismatch: Firmware may be corrupted.")
