from datetime import datetime
from requests.models import HTTPError

from BBOracle import project, project_logging
from BBOracle.auth import AuthManager
from BBOracle.url_builder import BestBuyURLBuilder
from BBOracle.api_requests import lookup as lookup_requests

class APIManager():
	"""
	Manages all API requests, their frequency and response.

	Properties:
		MAX_REQUEST_FREQ (int): Maximum number of requests per second.
	
	Attributes:
		paths (project.Paths): Object that manages file paths for this APIManager.
		env (project.Environment): Objects that determines the environment the APIManager is running in.
		auth_manager (auth.AuthManager): Authentication manager for this API Manager.
		last_req_time (datetime): The time of the last request made.
	"""
	MAX_REQUEST_FREQ = 1

	def __init__(self, paths=None, env=None, auth_mgr=None):
		self.paths = project.Paths() if paths is None else paths
		self.env = project.Environment(self.paths.environment_path) if env is None else env
		self.auth_manager = AuthManager(project.Auth(self.paths, self.env)) if auth_mgr is None else auth_mgr
		self.last_req_time = None
		self.refresh_jwt()

	def _max_freq_delay(self):
		"""
		Forces the thread to sleep for as long as is required to stay below our maximum request frequency.
		"""

		import time
		from datetime import datetime, timedelta
		time_of_req = datetime.now()
		if self.last_req_time is not None:
			# Get the difference in milliseconds between current time of request and previous.
			time_since_last_req = (time_of_req - self.last_req_time).total_seconds()
			if time_since_last_req < APIManager.MAX_REQUEST_FREQ:
				time.sleep(time_since_last_req)


	def _pre_request_routine(self):
		"""
		All actions that must be conducted before a request can be made.
		"""
		self._max_freq_delay()
		if not self.is_authenticated():
			self.refresh_jwt()

	def refresh_jwt(self):
		"""
		Refreshes the token.
		"""

		self._max_freq_delay()
		self.auth_manager.refresh_token()

	def is_authenticated(self):
		"""
		Determines if this APIManager is authenticated.

		Returns:
			bool: True if authenticated, False otherwise.
		"""
		return self.auth_manager.jwt_is_generated() and not self.auth_manager.is_expired()


	def request_usage(self):
		"""
		Makes a request to the usage statistics endpoint.
		https://documenter.getpostman.com/view/7012197/SVYwLGXM?version=latest#537ec7a5-55a8-44a0-ae05-c76f252066c5

		Returns:
			dict: JSON dict response of the request.
		"""

		# Conduct pre-request actions.
		self._pre_request_routine()
		req = lookup_requests.Usage(self.auth_manager)
		req.send_request()
		return req.response_json
	
	def send_request(self, req_obj):
		"""
		Sends a request using the inputted request object.

		Args:
			req_obj (api_requests.api_request.APIRequest): APIRequest object to send.
		"""

		# Conduct all pre-request actions.
		self._pre_request_routine()

		# After pre request actions, set the time of the last req to right now.
		self.last_req_time = datetime.now()

		# Make request
		req_obj.send_request()


		

	