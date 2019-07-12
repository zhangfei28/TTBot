#coding:utf-8
import sys
import config
import logging

__all__ = ['getLogger']

def getLogger(name):
    logger = Logger(name)
    return logger.logger

class Logger(object):

    settings = None
    encoding = 'utf-8'

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self,name):
        self.logger = logging.getLogger(name)
        self._set_logger(self.logger)

    def _set_logger(self,logger):
        logger.setLevel(logging.DEBUG)
        if logger.hasHandlers():
            return
        for i in self._get_handlers():
            logger.addHandler(i)

    @classmethod
    def _get_handlers(cls):
        enabled = config.LOG_ENABLE
        handlers = []
        if enabled:
            _level = config.LOG_LEVEL
            f_path = config.LOG_FILE_SAVE_PATH
            encoding = config.LOG_FILE_ENCODING
            _formatter = config.LOG_FORMAT[_level]
            _datefmt = config.LOG_DATE_FORMAT
            level = getattr(logging,_level)
            formatter = logging.Formatter(_formatter,datefmt=_datefmt)
            if f_path:
                encoding = encoding if encoding else cls.encoding
                f_handler = logging.FileHandler(f_path,
                                                encoding=encoding)
                f_handler.setLevel(logging.DEBUG)
                f_handler.setFormatter(formatter)
                handlers.append(f_handler)
            s_handler = logging.StreamHandler(stream=sys.stdout)
            s_handler.setLevel(level)
            s_handler.setFormatter(formatter)
            handlers.append(s_handler)
        else:
            handlers.append(logging.NullHandler())
        return handlers



