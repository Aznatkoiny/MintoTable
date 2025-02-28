"""
Application configuration settings
"""
import os

# OpenAI API configuration
OPENAI_MODEL = "gpt-4o-2024-08-06"

# File naming configuration
DEFAULT_FILENAME_PREFIX = "Project_Items"
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# Output directory (create if it doesn't exist)
OUTPUT_DIR = ""
if OUTPUT_DIR and not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# UI configuration
UI_WINDOW_TITLE = "Meeting Minutes to Project Plan Processor"
UI_WINDOW_SIZE = "900x800"
UI_INPUT_HEIGHT = 15
UI_RESULT_HEIGHT = 20

# Data validation handling
VALIDATE_FIELDS = True