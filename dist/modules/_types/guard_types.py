from typing import TypedDict, List, Union




# Request Guard Result
# Whenever the Prediction API is interacted with, the request is validated
# and the arguments are proccessed and returned.
class IRequestGuardResult(TypedDict):
    # If this value is a string means there is an error and the request cannot be processed.
    error: Union[str, None]

    # Epoch ID
    epoch_id: Union[str, None]

    # The list of synced close prices
    close_prices: List[float]