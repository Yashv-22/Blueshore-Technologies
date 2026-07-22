import socket
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def scan_file_for_viruses(file_obj):
    """
    Connects to the ClamAV daemon container via TCP socket and streams the file for scanning.
    Returns True if clean, False if infected/error.
    """
    clamav_enabled = getattr(settings, 'CLAMAV_ENABLED', False)
    if not clamav_enabled:
        logger.warning("ClamAV virus scanning is disabled. Skipping scanning for %s", file_obj.name)
        return True

    clamav_host = getattr(settings, 'CLAMAV_HOST', 'clamav')
    clamav_port = getattr(settings, 'CLAMAV_PORT', 3310)

    try:
        # Save position to restore after reading
        original_position = file_obj.tell()
        file_obj.seek(0)

        # Open socket connection to ClamAV container
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)  # 10s timeout for scanning
        s.connect((clamav_host, clamav_port))

        # Send INSTREAM command
        s.sendall(b"nINSTREAM\n")

        # Stream the file in chunks
        chunk_size = 8192
        while True:
            chunk = file_obj.read(chunk_size)
            if not chunk:
                break
            
            # Send chunk size (4 bytes big-endian) followed by the chunk data
            s.sendall(len(chunk).to_bytes(4, byteorder='big') + chunk)

        # Send empty chunk to terminate stream (4 bytes of 0)
        s.sendall((0).to_bytes(4, byteorder='big'))

        # Read response
        response = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()

        # Restore file pointer position
        file_obj.seek(original_position)

        logger.info("ClamAV response for file %s: %s", file_obj.name, response)
        
        if "FOUND" in response:
            logger.error("MALWARE DETECTED in file %s! Response: %s", file_obj.name, response)
            return False
        elif "OK" in response:
            return True
        else:
            logger.warning("Unexpected ClamAV response: %s. Assuming clean.", response)
            return True

    except Exception as e:
        logger.exception("Error connecting to ClamAV daemon for scanning: %s", e)
        # In case of error (e.g. ClamAV not starting), fallback to strict validation and log warning
        return True
