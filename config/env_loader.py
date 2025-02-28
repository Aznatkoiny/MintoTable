"""
Environment variable loader
Loads environment variables from .env file
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    """
    Load environment variables from .env file
    
    Returns:
        bool: True if .env file was found and loaded, False otherwise
    """
    # Try to find .env file in current directory or parent directories
    env_path = Path('.') / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        return True
    
    # Also check one level up (in case running from a subdirectory)
    parent_env_path = Path('..') / '.env'
    if parent_env_path.exists():
        load_dotenv(dotenv_path=parent_env_path)
        return True
    
    return False

def get_env_var(var_name, default=None):
    """
    Get environment variable with fallback to default
    
    Args:
        var_name (str): Name of the environment variable
        default: Default value if environment variable is not set
        
    Returns:
        Value of environment variable or default
    """
    return os.environ.get(var_name, default)