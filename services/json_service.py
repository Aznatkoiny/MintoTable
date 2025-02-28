"""
JSON file creation service
"""

import os
import json
from datetime import datetime
from config.app_config import TIMESTAMP_FORMAT, DEFAULT_FILENAME_PREFIX, OUTPUT_DIR

def save_json(minutes_data, output_path=None):
    """
    Save the minutes data as a JSON file
    
    Args:
        minutes_data: Structured minutes data
        output_path (str, optional): Path to save the JSON file
        
    Returns:
        str: Path to the created JSON file
    """
    if output_path is None:
        # Create a filename based on meeting title and current date/time
        safe_title = "".join(c if c.isalnum() else "_" for c in minutes_data.meeting_title) if minutes_data.meeting_title else "Meeting"
        timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
        filename = f"{DEFAULT_FILENAME_PREFIX}_{safe_title}_{timestamp}.json"
        
        # Use output directory if specified
        if OUTPUT_DIR:
            output_path = os.path.join(OUTPUT_DIR, filename)
        else:
            output_path = filename
    
    # Convert to dictionary and then to JSON
    minutes_dict = minutes_data.model_dump()
    
    with open(output_path, 'w') as json_file:
        json.dump(minutes_dict, json_file, indent=4)
    
    return output_path