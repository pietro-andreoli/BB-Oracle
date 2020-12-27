class BestBuyURLBuilder():
	"""
	A simple URL builder specifically for BestBuy API URLs.

	Example:
		path_parts = ["search", "contact"]
		url_obj = BestBuyURLBuilder(path_parts)
		print(url_obj.url)
		
		url_obj = BestBuyURLBuilder()
		url_obj.set_path("search", "contact")
		print(url_obj.url)
	
	Properties:
		PROTOCOL (str): Protocol of the URL.
		API_DOMAIN (str): Domain of the URL.
	
	Attributes:
		path_components (list): Path components separated.
		_url (str): The URL as a string.
	"""

	PROTOCOL = "https"
	API_DOMAIN = "api.bestbuy.com"

	def __init__(self, *args):
		self.path_components = []
		self.set_path(*args)
		self._url = None
		self._compile_url()

	def set_path(self, *args):
		"""
		Sets the path.
		"""

		self.path_components = args

	def _compile_url(self):
		"""
		Actually builds and sets the URL string.
		"""

		base_url = f"{BestBuyURLBuilder.PROTOCOL}://{BestBuyURLBuilder.API_DOMAIN}/"
		path = '/'.join(self.path_components)
		self._url = base_url + path

	@property
	def url(self):
		"""
		Getter for _url. Compiles the URL, sets it and returns it.

		Returns:
			str: Compiled URL.
		"""

		self._compile_url()
		return self._url
	
