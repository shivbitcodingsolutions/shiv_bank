import logging

def setup_logger(log_file_name="bank.log", log_level=logging.DEBUG):
    """
    Sets up a custom logger with a file handler and a console handler
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(log_file_name)

    c_handler.setLevel(log_level)
    f_handler.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d')
    c_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)

    # Add handlers to the logger
    if not logger.handlers: 
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger

# just for testing
# if __name__ == "__main__":
#     my_logger = setup_logger()
#     my_logger.info("This is msg 1 for testing")
#     my_logger.warning("This is msg 2 for testing")

