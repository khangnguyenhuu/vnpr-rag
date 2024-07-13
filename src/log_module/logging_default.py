# author: Khangnh
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class BaseLogger:
    def __init__(self, log_dir='logs', log_level=logging.INFO):
        self.log_dir = log_dir
        self.log_level = log_level

        # Create the log directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)

        ingest_log_dir = os.path.join(log_dir, 'ingest')
        os.makedirs(ingest_log_dir, exist_ok=True)

        llm_log_dir = os.path.join(log_dir, 'llm')
        os.makedirs(llm_log_dir, exist_ok=True)

        # Configure the logger ingest logger
        self.ingest_logger = logging.getLogger("ingest")
        self.ingest_logger.setLevel(self.log_level)
        log_file_ingest = os.path.join(ingest_log_dir, f'{datetime.now().strftime("%Y-%m-%d")}.log')
        file_handler_ingest = TimedRotatingFileHandler(log_file_ingest, when='midnight', backupCount=7)
        formatter_ingest = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler_ingest.setFormatter(formatter_ingest)
        self.ingest_logger.addHandler(file_handler_ingest)

        # Configure the logger llm logger
        self.llm_logger = logging.getLogger("llm")
        self.llm_logger.setLevel(self.log_level)
        log_file_llm = os.path.join(llm_log_dir, f'{datetime.now().strftime("%Y-%m-%d")}.log')
        file_handler_llm = TimedRotatingFileHandler(log_file_llm, when='midnight', backupCount=7)
        formatter_llm = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler_llm.setFormatter(formatter_llm)
        self.llm_logger.addHandler(file_handler_llm)

    # def debug(self, message, exc_info=None):
    #     self.logger.debug(message, exc_info=exc_info)

    # def info(self, message):
    #     self.logger.info(message)

    # def warning(self, message):
    #     self.logger.warning(message)

    # def error(self):
    #     self.logger.error(traceback.format_exc())

    # def critical(self, message):
    #     self.logger.critical(message)
# logger = BaseLogger(log_dir='logs', log_level=logging.DEBUG)
# logger.ingest_logger.info('This is an info message')
# logger.llm_logger.warning('This is a warning message')