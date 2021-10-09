import logging
from logging import FileHandler, Formatter

import settings

handlers = logging.getLogger(f"{settings.APP_NAME}.handlers")
middlewares = logging.getLogger(f"{settings.APP_NAME}.middlewares")
filters = logging.getLogger(f"{settings.APP_NAME}.filters")
utils = logging.getLogger(f"{settings.APP_NAME}.utils")
services = logging.getLogger(f"{settings.APP_NAME}.services")


def _logger_init(logger: logging.Logger):
    fmt = Formatter(
        fmt='%(levelname)s | %(asctime)s | %(name)s | %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler_info = FileHandler(filename=f'{settings.LOGS_DIR}/{settings.START_TIME}/{logger.name}.log',)
    handler_info.setFormatter(fmt=fmt)
    logger.addHandler(handler_info)


def setup():
    logging.basicConfig(
        encoding='UTF-8',
        level=logging.DEBUG,
        format='%(levelname)s | %(asctime)s | %(name)s | %(filename)s:%(lineno)d - %(message)s'
    )

    _logger_init(logger=handlers,)
    _logger_init(logger=middlewares,)
    _logger_init(logger=filters,)
    _logger_init(logger=utils,)
    _logger_init(logger=services,)
