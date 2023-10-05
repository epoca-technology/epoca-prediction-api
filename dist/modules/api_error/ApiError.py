from typing import Union, Any
from modules.utils.Utils import Utils
from modules.database.Database import TN, write_query










def log(origin: str, error: Any, params: Union[dict, None] = None) -> None:
    """Saves an API Error Into the Database. Notice that the uid and ip parameters are not meant to
    be provided as these values are only relevant in the Core API.

    IMPORTANT: This function is executed safely even if an error is raised, the function will
    complete and the error will be printed on the console.

    Args:
        origin: str
            The origin of the raised error. F.e: AuthRoute.createUser
        error: Any
            The error that was raised.
        params: Union[dict, None]
            The parameters that triggered the error.
    """
    try:
        write_query(
            f"INSERT INTO {TN['api_errors']}(o, e, c, uid, ip, p) VALUES (%s, %s, %s, %s, %s, %s)",
            (origin, str(error), Utils.get_time(), None, None, params)
        )
    except Exception as e:
        Utils.print(f"API Error was not logged: {str(e)}")