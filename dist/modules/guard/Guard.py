from typing import Union, List
from modules._types import IRequestGuardResult
from modules.environment.Environment import ENV
from modules.utils.Utils import Utils



# Request Guard Checker
def check_request(
    secret: Union[str, None],
    epoch_id: Union[str, None],
    close_prices: Union[List[float], None]
) -> IRequestGuardResult:
    """Given the API secret and a series of request arguments, it will validate,
    format and return the result in a dict format.

    Args:
        secret: Union[str, None]
            The API secret used by the Core API in order to interact 
            with the prediction API.
        epoch_id: Union[str, None]
            The ID of the active Epoch.
        close_prices: Union[List[float], None]
            The list of close prices that will be used to build the input dataset.

    Returns:
        IRequestGuardResult
    """
    # Init the result dict
    res: IRequestGuardResult = {
        "error": None,
        "epoch_id": epoch_id,
        "close_prices": close_prices
    }

    # Validate the provided secret
    if not isinstance(secret, str) or secret != ENV["FLASK_SECRET_KEY"]:
        res["error"] = f"The secret provided in the request is invalid."

    # Validate the Epoch ID
    if not isinstance(epoch_id, str) or epoch_id[0] != "_" or len(epoch_id) < 4 or len(epoch_id) > 100:
        res["error"] = f"The provided Epoch ID {epoch_id} is invalid."

    # Validate the list of close prices
    if not isinstance(close_prices, list) or len(close_prices) == 0:
        Utils.print(close_prices)
        res["error"] = f"The provided list of close prices is invalid."

    # Finally, return the result
    return res