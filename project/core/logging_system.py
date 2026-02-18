import logging
from logging.handlers import RotatingFileHandler
import os
from os import path
from datetime import datetime


class SystemLogger:
    VALID_LOG_TYPES = {'debug', 'info', 'warning', 'error', 'critical'}

    def __init__(self, log_type:str, title:str, data:str, *args, **kwargs):
        self.REPORTS_DIR = path.abspath(path.join(path.dirname(__file__), '..', 'reports'))

        self.LOGS_DIR = path.join(self.REPORTS_DIR, 'logs')
        if not path.exists(self.LOGS_DIR):
            os.mkdir(self.LOGS_DIR)

        self.today_logs = path.join(self.REPORTS_DIR, 'logs', str(datetime.today().date()))

        #- configurate logger system when class called -#
        self.logger = self._setup_logger()
        #- make class callable dirrectly by run _log func -#
        self._log(log_type, title, data)


    #--------------- logger system ---------------#
    def _setup_logger(self):
        #- create the LOGS folder -#
        if not path.exists(self.today_logs):
            os.mkdir(self.today_logs)


        #- logs settings -#
        logger = logging.getLogger('PortSpecter')
        logger.setLevel(logging.DEBUG)
        if logger.handlers:
            return logger   #- stop repeating
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


        #- File handler name
        exist_files = [file.split('.')[0][-1] for file in os.listdir(self.today_logs)]
        
        if not exist_files:
            file_name = 1
        else:
            file_name = int(exist_files[-1]) + 1
        
        file_name = path.join(self.today_logs, f'{datetime.now().strftime("%H-%M-%S")}_{file_name}.log')
        
        file_handler = RotatingFileHandler(
            file_name, maxBytes=5_000_000, backupCount=3
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


        #- consol handler
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.INFO)
        # console_handler.setFormatter(formatter)
        # logger.addHandler(console_handler)
        
        return logger


    #--------------- logger ---------------#
    def _log(self, log_type:str, title:str, data:str): #-> log types : debug - info - warning - error critical
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
            log_method(f'| {title} | ---> {data}')



# SystemLogger('debug', 'test', 'for test!')                             



