import os

# General
SHARED_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(os.path.dirname(__file__), "..")
ROOT_DIR = os.path.join(SRC_DIR, "..")
DATA_DIR = os.path.join(SRC_DIR, "data")
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")

# BaseX
DATABASE_NAME = "default"
