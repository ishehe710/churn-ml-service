import structlog

structlog.configure(
    processors=[
        structlog.processors.add_log_level,      # Adds 'level': 'info'
        
        # utc param allows machine local timezone
        structlog.processors.TimeStamper(fmt="iso",  utc=False), # Adds 'timestamp': '2026-01-06T16:16:00Z'
        structlog.processors.JSONRenderer()      # Converts to JSON string
    ]
)

# local logger for a file
def get_logger(name: str):
    return structlog.get_logger(name)
