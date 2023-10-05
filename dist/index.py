from typing import Union
from os.path import isfile
from flask import Flask, jsonify, request
from modules._types import IPrediction, IRequestGuardResult
from modules.utils.Utils import Utils
from modules.environment.Environment import ENV
from modules.guard.Guard import check_request
from modules.api_error.ApiError import log
from modules.epoch.Epoch import Epoch




# Flask App
# The process is binded to Flask in order to be exposed to the Core API.
app = Flask(__name__)









# Predict Route
# This route generates predictions and returns them inside of an API Response
# object. Prior to predicting, it makes sure the Prediction Model is 
# properly setup.
@app.route("/predict", methods=["POST"])
def predict():
    """Verifies the active epoch's integrity and makes any neccessary adjustments.
    Afterwards, it generates and prediction and returns it.

    Header:
        secret-key: str
            The secret required for the Core API to communicate with the Prediction API.

    Args:
        epoch_id: str
            The identifier of the Epoch.
        close_prices: List[float]
            The list of close prices that will be used to build the input dataset.

    Returns:
        IAPIResponse<IPrediction>
    """
    # Extract the request
    req_data: dict = request.get_json()

    # Firstly, check the request
    req: IRequestGuardResult = check_request(
        secret=request.headers.get("secret-key"),
        epoch_id=req_data.get("epoch_id"),
        close_prices=req_data.get("close_prices")
    )

    # Ensure the request can proceed
    if not isinstance(req["error"], str):
        # Generate the prediction safely
        try:
            # Generate the prediction
            pred: IPrediction = Epoch.generate_prediction(
                epoch_id=req["epoch_id"], 
                close_prices=req["close_prices"]
            )

            # Return it wrapped in an API Response
            return jsonify(Utils.api_response(pred))

        # If an error is raised, save the error and return it in an API response
        except Exception as e:
            # Log the api error
            log("PredictionAPI.predict", e)

            # Return the api error response
            return jsonify(Utils.api_response(error=e))

    # Otherwise, return the error
    else:
        return jsonify(Utils.api_response(error=req["error"]))









# Initializer
# Exposes the Prediction API to the Core API and displays general information about what is
# being served.
if __name__ == "__main__":
    from waitress import serve
    from paste.translogger import TransLogger
    from tensorflow import config, __version__ as tf_version

    # Initialize the # of GPUs available
    gpus_available: int = len(config.list_physical_devices("GPU"))

    # Retrieve the version of the API
    api_version: str = ""
    if not isfile("api_version.txt"):
        raise RuntimeError("The api_version.txt could not be loaded.")
    with open("api_version.txt") as version_file:
        api_version = version_file.read()

    # Welcome Message
    Utils.print("Prediction API Initialized")
    Utils.print(f"Running: v{api_version}")
    Utils.print(f"TensorFlow: v{tf_version}")
    Utils.print(f"Port: {ENV['PORT']}")
    Utils.print(f"Production: {ENV['production']}")
    if ENV["test_mode"]:
        Utils.print("Test Mode: True")
    if ENV["debug_mode"]:
        Utils.print("Debug Mode: True")
    if ENV["restore_mode"]:
        Utils.print("Restore Mode: True")
    Utils.print(f"GPUs Available: {gpus_available}")

    # Serve the API
    serve(TransLogger(app, setup_console_handler=False), host=ENV["FLASK_RUN_HOST"], port=ENV["PORT"])