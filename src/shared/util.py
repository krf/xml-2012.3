from ConfigParser import SafeConfigParser
from shared import constants
import logging
import os
import shutil

def setupLogger():
    # create logger
    logger = logging.getLogger("default")
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    #formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger

def setupOptions():
    # read options file initially
    options = SafeConfigParser()

    # read defaul config
    defaultConfig = constants.DEFAULT_CONFIG
    options.read(defaultConfig)

    # read per-user config
    userConfig = constants.USER_CONFIG
    if not os.path.isfile(userConfig):
        shutil.copy(defaultConfig, userConfig)
    options.read(userConfig)
    return options

# global logging instance
log = setupLogger()
options = setupOptions()
