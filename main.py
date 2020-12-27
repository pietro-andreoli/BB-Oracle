from BBOracle import project
from BBOracle import project_logging

ENV_OBJ = None
AUTH_OBJ = None
PATHS_OBJ = None

if __name__ == "__main__":
	project_logging.initialize_logger()
	logger = project_logging.module_logger("main")
	logger.info("Starting program...")
	PATHS_OBJ = project.Paths()
	ENV_OBJ = project.Environment(PATHS_OBJ.environment_path)
	logger.info(f"Session started in environment {ENV_OBJ.get_environment()}.")
	AUTH_OBJ = project.Auth(PATHS_OBJ, ENV_OBJ)
	logger.info("Stopping program...")