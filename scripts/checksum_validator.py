"""SHA-256 checksum verification for firmware integrity."""

import hashlib
from config import NEW_FIRMWARE_PATH, DEVICE_FIRMWARE_PATH


def sha256(path):
    """Calculate SHA-256 hash of a file.

    Args:
        path (Path): Path to the file.

    Returns:
        str: Hex digest of the file hash.
    """
    sha = hashlib.sha256()
    with open(path, 'rb') as file:
        while chunk := file.read(8192):
            sha.update(chunk)
    return sha.hexdigest()


if __name__ == "__main__":
    new_hash = sha256(NEW_FIRMWARE_PATH)
    installed_hash = sha256(DEVICE_FIRMWARE_PATH)

    if new_hash == installed_hash:
        print("Checksum match: Firmware integrity validated.")
    else:
        print("Checksum mismatch: Firmware may be corrupted.")
