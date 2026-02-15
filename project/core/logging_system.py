import logging
from logging.handlers import RotatingFileHandler
import os
from os import path
from datetime import datetime


class SystemLogger:
    VALID_LOG_TYPES = {'debug', 'info', 'warning', 'error', 'critical'}

    def __init__(self, log_type:str, data:str, *args, **kwargs):
        self.REPORTS_DIR = path.abspath(path.join(path.dirname(__file__), '..', 'reports'))
        self.LOGS_DIR = path.join(self.REPORTS_DIR, 'logs')
        #- configurate logger system when class called -#
        self.logger = self._setup_logger()
        #- make class callable dirrectly by run _log func -#
        self._log(log_type, data)


    #--------------- logger system ---------------#
    def _setup_logger(self):
        #- create the LOGS folder -#
        if not path.exists(self.LOGS_DIR):
            os.mkdir(self.LOGS_DIR)


        #- logs settings -#
        logger = logging.getLogger('PortSpecter')
        logger.setLevel(logging.DEBUG)
        if logger.handlers:
            return logger   #- stop repeating
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


        #- File handler
        file_name = path.join(self.LOGS_DIR,
                f'scan_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
                )
        file_handler = RotatingFileHandler(
            file_name, maxBytes=5_000_000, backupCount=3
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


        #- consol handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger


    #--------------- logger ---------------#
    def _log(self, log_type:str, data:str): #-> log types : debug - info - warning - error critical
        log_type = log_type.lower()

        #- make sure the logger has correct log_type -#
        if not hasattr(self.logger, log_type):
            #: close handler to remove empty file :#
            for handler in self.logger.handlers[:]:
                handler.close()
                self.logger.removeHandler(handler)

            files = [f for f in os.listdir(self.LOGS_DIR)]
            empty_file = path.join(self.LOGS_DIR, files[-1])
            os.remove(empty_file)
            print('log_type no available!')
            

        else:
            log_method = getattr(self.logger, log_type)
            log_method(data)



# SystemLogger('debug', 'for test!')
