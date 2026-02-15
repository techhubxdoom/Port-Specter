import logging
from logging.handlers import RotatingFileHandler
import os
from os import path
from datetime import datetime


#--------------- logging system ---------------#
def system_logger():
    #- create the LOGS folder -#
    reports_dir = path.abspath(
                  path.join(path.dirname(__file__), '..', 'reports')
                )
    logs_dir = path.join(reports_dir, 'logs')
    if not path.exists(logs_dir):
        os.mkdir(logs_dir)

    #- notificatiions settings -#
    logger = logging.getLogger('PortSpecter')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    #- File handler
    file_name = path.join(logs_dir,
                          f'scan_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
                          )
    file_handler = RotatingFileHandler(
        file_name, maxBytes=5_000_000, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    #- show messages in console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


#--------------- logger warpper ---------------#
logger = system_logger()

def _logger(log_type:str, data:str): #-> log types : debug - info - warning - error critical
    log_type = log_type.lower()

    #- make sure the logger has log_type function -#
    if not hasattr(logger, log_type):
        raise ValueError(
                    f"[LOGGER ERROR] Invalid log level '\033[31m{log_type}\033[0m'."
                    "Allowed logs types :"
                    "\033[32mdebug - info - warning - error - critical.\033[0m"
                    )
    
    log_method = getattr(logger, log_type)
    log_method(data)


_logger('ss', 'asdasdasd')
    
