import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

logs_path = os.path.join(os.getcwd(), 'logs')
os.makedirs(logs_path, exist_ok=True)
log_file_path = os.path.join(logs_path, LOG_FILE)
logging.basicConfig(level=logging.INFO,
                    filename=log_file_path,
                    format='%(asctime)s - %(levelname)s - %(lineno)d %(name)s - %(message)s')
