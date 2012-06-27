import os

# General
SHARED_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(os.path.dirname(__file__), "..")
ROOT_DIR = os.path.join(SRC_DIR, "..")
DATA_DIR = os.path.join(SRC_DIR, "data")
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")

# Config
DEFAULT_CONFIG = os.path.join(DATA_DIR, 'config.ini')
USER_CONFIG = os.path.expanduser('~/.xml2012.3.ini')

# BaseX
DATABASE_NAME = "default"
