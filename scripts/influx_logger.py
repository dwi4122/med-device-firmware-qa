"""Enhanced logging for medical device compliance."""

from influxdb import InfluxDBClient
from datetime import datetime
from typing import Dict, Any


class AuditLogger:
    """Handles audit logging for regulatory compliance."""
    
    def __init__(self):
        self.client = InfluxDBClient(
            host='localhost',
            port=8086,
            database='firmware_audit'
        )
    
    def log_event(self, event_type: str, metadata: Dict[str, Any]) -> None:
        """Log an auditable event with timestamp and metadata.
        
        Args:
            event_type: Type of event (e.g., firmware_update)
            metadata: Additional event details
        """
        try:
            log_entry = {
                "measurement": "device_events",
                "time": datetime.utcnow().isoformat(),
                "tags": {
                    "device_type": "CPAP",
                    "firmware_version": metadata.get('version', 'unknown')
                },
                "fields": {
                    "event_type": event_type,
                    **metadata
                }
            }
            self.client.write_points([log_entry])
        except Exception as e:
            print(f"Warning: Audit logging failed - {str(e)}")


# Create default logger instance
logger = AuditLogger()