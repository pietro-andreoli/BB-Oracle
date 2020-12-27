"""
This module is an encapsulation for all enums for the project.
"""

import json
import logging

def get_logger():
	"""
	Gets the logger for this module.

	Returns:
		Logger: The logger object for this module.
	"""

	return logging.getLogger("BestBuyAPI.project")

class Paths():
	"""
	A class for referencing all paths in the project. 
	If a path to a file is needed, an instance of this class should be used to get it.

	Attributes:
		PATHS_PATH (str): The only hardcoded path. A path to the file of paths.
	
	Properties:
		credentials_path (str): The path to the file containing API credentials.
		environment_path (str): The path to the file containing the current environment.
	"""

	PATHS_PATH = "BBOracle/paths.json"
	def __init__(self):
		path_dict = self._read_paths_file()
		self.credentials_path = path_dict["API_CREDENTIALS"]
		self.environment_path = path_dict["ENVIRONMENT"]
	
	def _read_paths_file(self):
		"""
		Reads the JSON file that defines all file paths.

		Raises:
			err: Raised when the file is missing or unreadable.

		Returns:
			dict: File paths in dict format.
		"""

		logger = get_logger()
		try:
			logger.info("Trying to read the paths file at %s", Paths.PATHS_PATH)
			with open(Paths.PATHS_PATH, 'r') as paths_f:
				path_json = json.load(paths_f)
				logger.info("Path file successfully read.")
				return path_json
		except BaseException as err:
			logger.exception("Could not read paths file!")
			raise err

class Auth():
	"""
	A class that manages the authentication of the project and API.
	Mainly this means handling credentials and tokens.
	"""

	def __init__(self, path_manager, environment):
		self.username = None
		self.password = None
		self.path_manager = path_manager
		self.environment = environment

	def creds_loaded(self):
		"""
		States whether this Auth object has its credentials loaded or not.

		Returns:
			bool: True if credentials loaded, False otherwise.
		"""

		return self.username is not None and self.password is not None

	def load_credentials(self):
		logger = get_logger()
		try:
			logger.info("Trying to read the credentials file at %s", self.path_manager.credentials_path)
			with open(self.path_manager.credentials_path, 'r') as cred_f:
				creds_dict = json.load(cred_f)
				self.username = creds_dict[self.environment.get_environment()]["username"]
				self.password = creds_dict[self.environment.get_environment()]["password"]
				logger.info("Credentials file successfully read.")
		except BaseException as err:
			logger.exception("Could not read credentials file!")
			raise err

class Environment():
	"""
	Class that represents the environment the project is currently running in.
	The class also acts as an enum for environment related information.
	"""

	PRODUCTION = "PRODUCTION"
	DEVELOPMENT = "DEVELOPMENT"

	def __init__(self, environment_path):
		self.env_path = environment_path
		self.environment = self.initialize_environment()

	def initialize_environment(self):
		logger = get_logger()
		try:
			logger.info("Trying to read the environment file at %s", self.env_path)
			with open(self.env_path, 'r') as env_f:
				environment = env_f.read().strip()
				logger.info("Environment file successfully read.")
				logger.info("Environment initialized as %s", environment)
				return environment
		except BaseException as err:
			logger.exception("Could not read credentials file!")
			raise err

	def get_environment(self):
		"""
		An all encapsulating function to get the environment.
		If not yet initialized, it will read the environment file to get the environment.

		Returns:
			str: The environment as a string. Possible options include Environment.PRODUCTION, Environment.DEVELOPMENT.
		"""

		if self.environment != Environment.PRODUCTION and self.environment != Environment.DEVELOPMENT:
			self.environment = self.initialize_environment(self.env_path)
		return self.environment