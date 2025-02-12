# app/utils.py

import logging
from datetime import datetime
import os

def setup_logging() -> None:
    """Configure logging to write to logs/app.log."""
    # Ensure the logs directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Configure logging
    logging.basicConfig(
        filename='logs/app.log',  # Log file path
        level=logging.INFO,       # Log level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
    )

def generate_student_id(name: str) -> str:
    """Generate a unique student ID using the student's name and current timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"STU{hash(name + timestamp)}"