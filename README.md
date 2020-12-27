# Introduction 
This repo manages authentication, communication, and post processing of all Best Buy API interaction.

# Build

This application was built using **Python 3.9.x**

To build this app you first set up the virtual environment. Please note that a virtual environment is not required, but is best practice when working with a Python repo. On Windows I use `virtualenv`, on Ubuntu the built in `venv` works just fine.
The following commands are for `virtualenv`

1. Install `virtualenv` using PIP.
	```
	python -m pip install --user virtualenv
	``` 

2. Navigate to where the virtual environment folder is to be created and run the following command.
	```
	virtualenv BestBuyAPI-venv
	```
	Note: BestBuyAPI-venv can be replaced with anything. It becomes the name of the virtual environment and the folder containing it.

3. Navigate into /BestBuyAPI-env and clone the repo at master.
	```
	git clone https://github.com/pietro-andreoli/BB-Oracle.git
	```

4. From here you can use your IDE and select the virtualenv interpreter for your development.
	- In VS Code use `ctrl + shift + P`, search "Python: Select Interpreter" and find the interpreter `.../BestBuyAPI-env/Scripts/python.exe`.
	**Your virtual environment must be activated for your scripts to use the correct interpreter and libraries.**

5. With the virtual environment activated you should install all necessary libraries at the specified versions.
	- No external libraries are required to build this project yet.

# Test
Tests can be found in any file matching the pattern `*_test.py`. Before pushing to production ensure all tests are successful by running those files.

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

# Project Goals
- [x] TODO: Create basics of API communication.

# Process Explanation
The process of querying an API endpoint begins at the `BBOracle.api_manager.APIManager` class.
Create an APIManager object
```Python
from BBOracle.api_manager import APIManager
api_mgr = APIManager()
```
Initialization of the API manager will do multiple things for you.

1. Read all the relevant file paths into memory using a `project.Paths` object.
2. Initialize the environment (dev vs prod) using a `project.Environment` object.
3. Load the API credentials into memory using a `project.Auth` object and manage a Java Web Token (JWT) using a `auth_manager.AuthManager` object.
	3.1. Fetch the JWT and manage it through the `AuthManager` object.

Lets say you want to check the usage of credits. Continuing from the previous code we'd add the following.

```Python
from BBOracle.api_requests import lookup
req = lookup.Usage(api_mgr.auth_manager)
self.api_manager.send_request(req)
print(req.response_json)
```

And the response of the request can be found in `req.response_json`