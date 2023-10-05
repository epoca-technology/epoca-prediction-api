from typing import List, Dict, Any
from unittest import TestCase, main
from time import time
from modules._types import IAPIResponse
from modules.environment.Environment import ENV
from modules.utils.Utils import Utils




# Unit tests can only be executed if the container is running in test mode
if not ENV["test_mode"]:
    raise Exception("Unit Tests can only be executed when the container is running in test mode.")





# Test Class
class UtilsTestCase(TestCase):
    # Before Tests
    def setUp(self):
        pass

    # After Tests
    def tearDown(self):
        pass









    ## API Response ##


    # Can build a proper API Response with and without data & errors
    def testAPIResponse(self):
        # Basic Response
        basic: IAPIResponse = Utils.api_response()
        self.assertTrue(isinstance(basic, Dict))
        self.assertTrue(basic["success"])
        self.assertTrue(basic["data"] is None)
        self.assertTrue(basic["error"] is None)

        # Response with list data 
        test_list: List = ["Hello", "There", 123456]
        with_list_data: IAPIResponse = Utils.api_response(test_list)
        self.assertTrue(isinstance(with_list_data, Dict))
        self.assertTrue(with_list_data["success"])
        self.assertTrue(isinstance(with_list_data["data"], List))
        self.assertListEqual(with_list_data["data"], test_list)
        self.assertTrue(with_list_data["error"] is None)

        # Response with dict data 
        test_dict: Dict[Any] = {
            "someString": "Hello There!",
            "someInt": 123456,
            "someFloat": 123456.236,
            "someBool": True,
            "someList": [1, 2, 3],
        }
        with_dict_data: IAPIResponse = Utils.api_response(test_dict)
        self.assertTrue(isinstance(with_dict_data, Dict))
        self.assertTrue(with_dict_data["success"])
        self.assertDictEqual(with_dict_data["data"], test_dict)
        self.assertTrue(with_dict_data["error"] is None)

        # Response with error
        err: str = "Wow this is an error...Sorry about that."
        with_error: IAPIResponse = Utils.api_response(error=err)
        self.assertTrue(isinstance(with_error, Dict))
        self.assertFalse(with_error["success"])
        self.assertEqual(with_error["error"], err)




    # Can attach a code to an error
    def testAPIError(self):
        self.assertEqual(Utils.api_error("Some error.", 0), "Some error. {(0)}")
        self.assertEqual(Utils.api_error("Some error.", 500000), "Some error. {(500000)}")










    ## Number Helpers ##



    # Can calculate the percentage change of a number
    def testGetPercentageChange(self):
        self.assertEqual(Utils.get_percentage_change(100, 150), 50)
        self.assertEqual(Utils.get_percentage_change(100, 50), -50)
        self.assertEqual(Utils.get_percentage_change(155.89, 199.63), 28.06)
        self.assertEqual(Utils.get_percentage_change(8559.63, 12455.87), 45.52)
        self.assertEqual(Utils.get_percentage_change(44785.12, 44521.33), -0.59)
        self.assertEqual(Utils.get_percentage_change(799415.88, 55121), -93.1)
        self.assertEqual(Utils.get_percentage_change(255446.69, 463551.11), 81.47)










    ## Time Helpers ##




    # Can retrieve the current time in milliseconds
    def testGetTime(self):
        current_time: float = time()
        self.assertAlmostEqual(Utils.get_time(), Utils.from_seconds_to_milliseconds(current_time), 5)





    # Can convert Milli Seconds into Seconds
    def testFromMilliSecondsToSeconds(self):
        self.assertEqual(Utils.from_milliseconds_to_seconds(1647469003036), 1647469003)
        self.assertEqual(Utils.from_milliseconds_to_seconds(1647469088126), 1647469088)
        self.assertEqual(Utils.from_milliseconds_to_seconds(1647469123651), 1647469123)
        self.assertEqual(Utils.from_milliseconds_to_seconds(1647469123651.5412), 1647469123)




    # Can convert Seconds into Milli Seconds
    def testFromSecondsToMilliSeconds(self):
        self.assertEqual(Utils.from_seconds_to_milliseconds(1647469003), 1647469003000)
        self.assertEqual(Utils.from_seconds_to_milliseconds(1647469088), 1647469088000)
        self.assertEqual(Utils.from_seconds_to_milliseconds(1647469123), 1647469123000)
        self.assertEqual(Utils.from_seconds_to_milliseconds(1647469123.1234), 1647469123123)



# Test Execution
if __name__ == "__main__":
    main()