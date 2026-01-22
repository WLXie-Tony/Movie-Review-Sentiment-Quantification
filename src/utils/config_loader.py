"""
Configuration Loader
~~~~~~~~~~~~~~~~~~~~
Provides a singleton interface to load and access project settings 
defined in config/settings.yaml.
"""

import yaml
from pathlib import Path
from typing import Dict, Any

# Define the path to the config file relative to this script
# Structure: src/utils/config_loader.py -> ... -> config/settings.yaml
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.yaml"

def load_config(config_path: Path = CONFIG_PATH) -> Dict[str, Any]:
    """
    Loads the YAML configuration file and returns it as a dictionary.

    Args:
        config_path (Path): Path to the settings.yaml file.

    Returns:
        Dict[str, Any]: Configuration dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        yaml.YAMLError: If the file contains invalid YAML syntax.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as f:
        try:
            config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as e:
            raise RuntimeError(f"Error parsing YAML configuration: {e}")

# Create a global instance for easy import
# Usage: from src.utils.config_loader import config
config = load_config()