import logging as pylogging
PARENT_LOGGER_NAME = "BestBuyAPI"
PARENT_LOGGER_FILE_PATH = "logs/BestBuyAPI.log"
PARENT_LOGGER_TESTING_FILE_PATH = "BestBuyAPI/logs/BestBuyAPITests.log"

def initialize_logger(testing=False):
	# create logger with 'spam_application'
	logger = pylogging.getLogger(PARENT_LOGGER_NAME)
	logger.setLevel(pylogging.DEBUG)
	# create file handler which logs even debug messages
	file_handler = pylogging.FileHandler(
		PARENT_LOGGER_FILE_PATH if not testing else PARENT_LOGGER_TESTING_FILE_PATH
	)
	file_handler.setLevel(pylogging.DEBUG)
	# create console handler with a higher log level
	console_handler = pylogging.StreamHandler()
	console_handler.setLevel(pylogging.DEBUG)
	# create formatter and add it to the handlers
	formatter = pylogging.Formatter("%(asctime)s : %(name)s : %(levelname)s : %(message)s")
	file_handler.setFormatter(formatter)
	console_handler.setFormatter(formatter)
	# add the handlers to the logger
	logger.addHandler(file_handler)
	logger.addHandler(console_handler)
	return logger

def module_logger(source_name):
	"""
	Gets the logger for a module/class. This function entirely depends on the source name.

	Example:
		module_logger("main") -> BestBuyAPI.main

	Args:
		source_name (str): Name for the logger, idealy the same as the source.

	Returns:
		Logger: Logging object, child of parent logger generated in logging.initialize_logger().
	"""

	return pylogging.getLogger(f"{PARENT_LOGGER_NAME}.{source_name}")