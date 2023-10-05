from unittest import TestCase, main
from typing import Dict, Any, List
from modules._types import IApiErrorRecord
from modules.environment.Environment import ENV
from modules.database.Database import TN, read_query, write_query
from modules.api_error.ApiError import log




# Unit tests can only be executed if the container is running in test mode
if not ENV["test_mode"]:
    raise Exception("Unit Tests can only be executed when the container is running in test mode.")



# Test Data
origin: str = "ApiErrorTestCase.test"
error_msg: str = "Oh no! There was a nasty error. We did something wrong :("







## Test Method Helpers ##



def _get_all() -> List[IApiErrorRecord]:
    """Retrieves all the API Errors currently stored in the Database.
    
    IMPORTANT: This method is only used for unit tests in the Forecast API.

    Args:
        None
    
    Returns:
        List[IApiErrorRecord]
    
    Raises:
        None
    """
    return read_query(f"SELECT * FROM {TN['api_errors']} ORDER BY c DESC")





def _delete_all() -> None:
    """Deletes all the API Errors currently stored in the database.

    IMPORTANT: This method is only used for unit tests in the Forecast API.

    Args:
        None
    
    Returns:
        None
    
    Raises:
        None
    """
    write_query(f"DELETE FROM {TN['api_errors']}")






# Test Class
class ApiErrorTestCase(TestCase):
    # Before Tests
    def setUp(self):
        _delete_all()
        

    # After Tests
    def tearDown(self):
        _delete_all()
        




    # Can save an error without any parameters
    def testErrorWithoutParameters(self):
        # In the beginning....there were no logs
        errors: List[IApiErrorRecord] = _get_all()
        self.assertEqual(len(errors), 0)

        # Log the error
        log(origin, error_msg)

        # Retrieve all errors
        errors = _get_all()
        
        # Make sure there is 1 record
        self.assertEqual(len(errors), 1)

        # Validate the data integrity
        self.assertEqual(errors[0]["o"], origin)
        self.assertEqual(errors[0]["e"], error_msg)
        self.assertTrue(isinstance(errors[0]["c"], int))



    # Can save an error with parameters
    def testErrorWithParameters(self):
        # Init the dict
        dict: Dict[str, Any] = {
            "uid": "SomeCoolUID",
            "someCoolInt": 5,
            "someCoolFloat": 5.65,
            "someCoolBool": False,
            "someCoolList": [12.5, 13, 85.99],
        }

        # Log the error
        log(origin, error_msg, dict)

        # Retrieve all errors
        errors: List[IApiErrorRecord] = _get_all()

        # Make sure there is 1 record
        self.assertEqual(len(errors), 1)

        # Validate the data integrity
        self.assertEqual(errors[0]["o"], origin)
        self.assertEqual(errors[0]["e"], error_msg)
        self.assertTrue(isinstance(errors[0]["p"], Dict))
        self.assertDictEqual(dict, errors[0]["p"])
        self.assertTrue(isinstance(errors[0]["c"], int))



    # Can save an error from a raised exception
    def testErrorWithParametersFromException(self):
        # Init values
        o: str = "ApiErrorTestCase.testErrorWithParametersFromException"
        e: str = "This error should be logged in the API Errors Database."
        p: Dict[str, Any] = {
            "uid": "SomeCoolUID",
            "someCoolInt": 5,
            "someCoolFloat": 5.65,
            "someCoolBool": False,
            "someCoolList": [12.5, 13, 85.99],
        }

        # Raise an exception and catch it
        try:
            raise Exception(e)
        except Exception as error:
            # Log the error
            log(o, error, p)

            # Retrieve all errors
            errors: List[IApiErrorRecord] = _get_all()

            # Make sure there is 1 record
            self.assertEqual(len(errors), 1)

            # Validate the data integrity
            self.assertEqual(errors[0]["o"], o)
            self.assertEqual(errors[0]["e"], e)
            self.assertTrue(isinstance(errors[0]["p"], Dict))
            self.assertDictEqual(p, errors[0]["p"])
            self.assertTrue(isinstance(errors[0]["c"], int))




# Test Execution
if __name__ == "__main__":
    main()