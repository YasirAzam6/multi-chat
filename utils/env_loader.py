import os
from dotenv import load_dotenv

class EvnLoader:
    """
    A utility class to load environment variables from a .env file.
    """

    def __init__(self):
        load_dotenv()

    def get(self, key: str, default: str = None) -> str:
        """
        Retrieve the value of an environment variable.

        Args:
            key (str): The name of the environment variable.
            default (str, optional): The default value to return if the variable is not found. Defaults to None.

        Returns:
            str: The value of the environment variable or the default value.
        """
        return os.getenv(key, default)
    
env_loader = EvnLoader()