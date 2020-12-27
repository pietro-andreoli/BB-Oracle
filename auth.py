from zi_api_auth_client import user_name_pwd_authentication
from BBOracle import project
from BBOracle import main
from datetime import datetime
from datetime import timedelta

class JWT():
	"""
	A class that manages the necessary information of a Java Web Token (JWT).

	Attributes:
		token (str): The token string used for authentication.
		creation_t (datetime): 
	"""

	def __init__(self, jwt, creation_t):
		self.token = jwt
		self.creation_t = datetime.now()

class AuthManager():
	"""
	Represents the Authentication Manager for the application.
	Handles management of JWT, including refreshing.

	Behaviour:
		Creating an instance of this class does not automatically authenticate the object.
		To check if the object is authenticated, call jwt_is_generated().
		To authenticate the object, call its refresh_token() function.
	
	Properties:
		JWT_LIFE_LENGTH (int): The number of hours a JWT has before it expires. This is set by the API.

	Attributes:
		jwt (JWT): JWT object that holds the information of the current Java Web Token for Authentication.
		expire_offset: The time offset (in seconds) to consider the JWT expired. Basically, expire_time = creation_time + expire_offset
	"""

	JWT_LIFE_LENGTH = 1

	def __init__(self, auth_obj):
		"""
		Initializer for this class.

		Args:
			auth_obj (project.Auth): Possesses credentials for this manager.
		"""

		self.auth = auth_obj
		self.jwt = None
		self.expire_offset = -120
	
	def jwt_is_generated(self):
		"""
		Determines if the JWT for this object has been generated.

		Returns:
			bool: True if the JWT has been generated, False otherwise.
		"""

		return self.jwt is not None and self.jwt.token is not None and len(self.jwt.token) > 0

	def get_expire_time(self):
		"""
		Calculates the expiry time of the JWT based on its creation time, duration length and offset.

		Returns:
			datetime.datetime: Time that the JWT expires.
		"""
		if not self.jwt_is_generated():
			raise AuthManagerExceptions.JWTNotGenerated()
		return self.jwt.creation_t + timedelta(hours=1, seconds=self.expire_offset)

	def is_expired(self):
		"""
		Determines if the current token is expired.

		Returns:
			bool: True if the token has expired, False otherwise.
		"""

		return datetime.now() > self.get_expire_time()

	def init_token(self):
		"""
		A more descriptive function, used when first authenticating.
		The same as calling refresh_token()
		"""

		self.refresh_token()

	def refresh_token(self):
		"""
		Refreshes the authentication token.

		Parameters:
			username (str): Username for the API.
			password (str): Password for the API.

		Returns:
			str: Java Web Token.
		"""

		jwt_str = self._generate_jwt()
		self.jwt = JWT(jwt_str, datetime.now())

	def _generate_jwt(self):
		"""
		Uses the zi_auth_api to get a Java Web Token.

		Returns:
			str: Java Web Token.
		"""
		if not self.auth.creds_loaded():
			self.auth.load_credentials()
		return user_name_pwd_authentication(self.auth.username, self.auth.password)
	
	def get_token_str(self):
		"""
		Shortcut for getting the JWT token as a string.

		Returns:
			str: JWT as str.
		"""

		if not self.jwt_is_generated():
			raise AuthManagerExceptions.JWTNotGenerated()
		return self.jwt.token

class AuthManagerExceptions():
	class JWTNotGenerated(Exception):
		"""
		Raised when the JWT is referenced but has not been generated yet.
		"""
		pass