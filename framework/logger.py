import logging

logger = logging.getLogger('ecommerce-sdet')
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("logs/test.log")  # Add the loggers to logs/test.log file

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s"
)  # Formate the loggers for better readability

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)



logger.info("Logger is working!")