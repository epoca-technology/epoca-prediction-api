from typing import TypedDict, Optional, Any




# API Response
# Whenever the Prediction API is interacted with, the following response will
# be returned.
class IAPIResponse(TypedDict):
    success: bool
    data: Optional[Any]
    error: Optional[str]