from typing import TypedDict, Optional






# API Error Record
class IApiErrorRecord(TypedDict):
    o: str              # Origin (F.e: AuthRoute.createUser or CandlestickService.syncCandlesticks)
    e: str              # Error Message
    c: int              # Creation Time in Milliseconds
    uid: Optional[str]  # Request Sender UID
    ip: Optional[str]   # Request Sender IP
    p: Optional[dict]   # Params in json format used to trigger the error - Should be converted into a dictionary when retrieving