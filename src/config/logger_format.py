import logging


class CustomLogFormatter(logging.Formatter):
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    blue = "\x1b[36m"
    reset = "\x1b[0m"
    msg_formats = {
        "error": (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        ),
        "debug": ("%(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)"),
        "info": ("%(message)s"),
    }

    FORMATS = {
        logging.DEBUG: f"{yellow} {msg_formats['debug']} {reset}",
        logging.INFO: blue + msg_formats["info"] + reset,
        logging.WARNING: red + msg_formats["error"] + reset,
        logging.ERROR: red + msg_formats["error"] + reset,
        logging.CRITICAL: red + msg_formats["error"] + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
