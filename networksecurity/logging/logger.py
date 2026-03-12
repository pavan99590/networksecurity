# Sets up timestampled log file generation

import logging
import os
from datetime import datetime

# Creating a unique log file name based on the current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Defining the path for the logs directory and creating it if it doesn't exist
logs_path = os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)

# Final path for the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configuring the logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)