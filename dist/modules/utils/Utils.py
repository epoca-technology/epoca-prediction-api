from typing import Union, Optional, Any
from sys import stderr
from time import time
from modules._types import IAPIResponse






## Class ##
class Utils:
    """Utils Class

    This singleton provides a series of functionalities that simplify development and 
    provide consistency among modules.
    """






    ##################
    ## API Response ##
    ##################




    @staticmethod
    def api_response(data: Optional[Any] = None, error: Optional[Any] = None) -> IAPIResponse:
        """Builds a successful or unsuccessful API Response based on the provided arguments.

        Args:
            data: Optional[Any]
                The data to be returned in the request's response.
            error: Optional[Any]
                The error that has been raised. If provided, the success property will be set
                as false and the error will be converted into a string.

        Returns:
            IAPIResponse
        """
        return { "success": error is None, "data": data, "error": str(error) if error is not None else None }








    @staticmethod
    def api_error(error: Any, code: int) -> str:
        """Converts the error to a string and concatenates the error code with the correct format {(0)}.

        Args:
            error: Any
                The error raised or to be raised, can be an exception or a string.
            code: int
                The code to be concatenated to the error string.

        Returns:
            str
        """
        return str(error) + " {(" + str(code) + ")}"











    ####################
    ## Number Helpers ##
    ####################




    @staticmethod
    def get_percentage_change(old_value: float, new_value: float) -> float:
        """Calculates the percentage change a value has experienced.

        Args:
            old_value: float
                The original number to calculate the % change for.
            new_value: float
                The new state of the original number.

        Returns:
            float
        """
        # If the old value is zero, the percentage change cannot be calculated
        if old_value == 0:
            return 0
            
        # Init the change
        change: float = 0.0

        # Handle an increase
        if new_value > old_value:
            increase: float = new_value - old_value
            change = (increase / old_value) * 100

        # Handle a decrease
        elif old_value > new_value:
            decrease: float = old_value - new_value
            change = -((decrease / old_value) * 100)

        # Return the change
        return round(change if change >=-100 else -100, 2)














    ##################
    ## Time Helpers ##
    ##################






    @staticmethod
    def get_time() -> int:
        """Retrieves the current time in milliseconds. Equivalent of Javascript's Date.now().

        Returns:
            int
        """
        return Utils.from_seconds_to_milliseconds(time())











    @staticmethod
    def from_milliseconds_to_seconds(milliseconds: Union[int, float]) -> int:
        """Converts a milli seconds value into seconds. Notice that it will round
        decimals downwards in case of a float.

        Args:
            milliseconds: Union[int, float]
                The timestamp in milliseconds to be converted to seconds.

        Returns:
            int
        """
        return int(milliseconds / 1000)









    @staticmethod
    def from_seconds_to_milliseconds(seconds: Union[int, float]) -> int:
        """Converts a seconds value into milliseconds. Notice that it will round 
        decimals downwards in case of a float.

        Args:
            seconds: Union[int, float]
                The seconds timestamp to be converted to milliseconds.

        Returns:
            int
        """
        return int(seconds * 1000)






    @staticmethod
    def subtract_minutes(timestamp_ms: Union[int, float], minutes: int) -> int:
        """Subtracts minutes to a given timestamp. The output of this function is a 
        timestamp in milliseconds with the subtracted minutes.

        Args:
            timestamp_ms: Union[int, float]
                The original timestamp that will be decreased.
            minutes: int 
                The number of minutes that will be reduced from the timestamp.

        Returns:
            int
        """
        return int(timestamp_ms - (Utils.from_seconds_to_milliseconds(60) * minutes))






    @staticmethod
    def add_minutes(timestamp_ms: Union[int, float], minutes: int) -> int:
        """Adds minutes to a given timestamp. The output of this function is a 
        timestamp in milliseconds with the added minutes.

        Args:
            timestamp_ms: Union[int, float]
                The original timestamp that will be decreased.
            minutes: int 
                The number of minutes that will be added to the timestamp.

        Returns:
            int
        """
        return int(timestamp_ms + (Utils.from_seconds_to_milliseconds(60) * minutes))













    ##################
    ## Misc Helpers ##
    ##################






    @staticmethod
    def print(msg: str) -> None:
        """Prints a custom message into the console bypassing the log block imposed by Flask.

        Args:
            msg (str): The message to be printed.
        """
        print(msg, file=stderr)