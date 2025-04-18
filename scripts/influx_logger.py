from influxdb import InfluxDBClient

def log_event(event, fields):
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database("firmware_monitoring")
    payload = [{
        "measurement": event,
        "fields": fields
    }]
    client.write_points(payload)
