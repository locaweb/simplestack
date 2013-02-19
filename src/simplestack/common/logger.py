import logging
import logging.config
import logging.handlers


def set_logger():
    root_logger = logging.root
    root_logger.setLevel(logging.DEBUG)

    log_format = "[%(name)s] %(levelname)s - %(message)s"
    log_date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, log_date_format)

    SysLogHandler = logging.handlers.SysLogHandler

    try:
        handler = SysLogHandler(address='/dev/log',
                                facility=SysLogHandler.LOG_SYSLOG)
    except socket.error:
        handler = SysLogHandler(address='/var/run/syslog',
                                facility=SysLogHandler.LOG_SYSLOG)

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
