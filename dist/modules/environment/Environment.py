from typing import Any
from os import environ
from modules._types import IEnvironment





## ENVIRONMENT VALUE GETTERS ##






def _get_string(key: str) -> str:
    """Retrieves a string value from an environment property.

    Args:
        key (str): The key of the value in the system's environment

    Returns:
        str
    
    Raises:
        ValueError: If the environment key is not a valid string.
    """
    val: Any = environ[key]
    if isinstance(val, str) and len(val) > 0:
        return val
    else:
        raise ValueError(f"The environment key {key} is not a valid string ({str(type(val))}: {str(val)}).")

        




def _get_integer(key: str) -> int:
    """Retrieves an integer value from an environment property.

    Args:
        key (str): The key of the value in the system's environment

    Returns:
        int
    
    Raises:
        ValueError: If the environment key is invalid or cannot be converted to int.
    """
    val: str = _get_string(key)
    try:
        return int(val)
    except ValueError:
        raise ValueError(f"The environment key {key} could not be converted to integer ({str(type(val))}: {val}).")












## ENVIRONMENT INITIALIZATION ##




ENV: IEnvironment = {
    "production": _get_string("NODE_ENV") == "production",
    "test_mode": _get_string("testMode") == "true",
    "debug_mode": _get_string("debugMode") == "true",
    "restore_mode": _get_string("restoreMode") == "true",
    "POSTGRES_HOST": _get_string("POSTGRES_HOST"),
    "POSTGRES_USER": _get_string("POSTGRES_USER"),
    "POSTGRES_PASSWORD": _get_string("POSTGRES_PASSWORD"),
    "POSTGRES_DB": _get_string("POSTGRES_DB"),
    "FLASK_RUN_HOST": _get_string("FLASK_RUN_HOST"),
    "FLASK_SECRET_KEY": _get_string("FLASK_SECRET_KEY"),
    "PORT": _get_integer("PORT")
}