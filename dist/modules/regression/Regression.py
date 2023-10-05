from typing import List
from random import seed
from numpy.random import seed as npseed
from tensorflow import random as tf_random
from numpy import ndarray
from h5py import File as h5pyFile
from tensorflow.python.keras.saving.hdf5_format import load_model_from_hdf5
from keras import Sequential
from modules.utils.Utils import Utils






class Regression:
    """Regression Class

    This class handles the initialization and management of a Keras Regression Model.

    Class Properties:
        MODEL_PATH: str
            The path to the volume in which the regression model files are located.
        MIN_FEATURE_VALUE: float = 0.01
        MAX_FEATURE_VALUE: float = 3
            The minimum and maximum values features are allowed to have.

    Instance Properties:
        id: str
            The ID of the model that was set when training.
        description: str
            Important information regarding the trained model.
        lookback: int
            The number of prediction candlesticks that will be used to generate predictions.
        predictions: int
            The number of predictions to be generated.
        model: Sequential
            The instance of the trained model.
    """
    # The path in which the regression model files are located
    MODEL_PATH: str = "/var/lib/epoch"

    # Min and max feature values
    MIN_FEATURE_VALUE: float = 0.01
    MAX_FEATURE_VALUE: float = 1






    ####################
    ## Initialization ##
    ####################



    def __init__(self, id: str, epoch_seed: int):
        """Initializes the Regression Instance.

        Args:
            id: str
                The ID of the model that will be initialized.
            epoch_seed: int
                The random seed of the Epoch that will be set on all required libs.

        Raises:
            ValueError:
                If there is an issue loading the model.
                If the ID stored in the model's file is different to the one provided.
                If any of the other metadata is invalid.
        """
        with h5pyFile(f"{Regression.MODEL_PATH}/{id}.h5", mode="r") as model_file:
            self.id: str = model_file.attrs["id"]
            self.description: str = model_file.attrs["description"]
            self.lookback: int = int(model_file.attrs["lookback"])          # Downcast to int
            self.predictions: int = int(model_file.attrs["predictions"])    # Downcast to int
            self.model: Sequential = load_model_from_hdf5(model_file)

        # Make sure the IDs are identical
        if self.id != id:
            raise ValueError(f"Regression ID Missmatch: {self.id} != {id}")

        # Make sure the description was extracted
        if not isinstance(self.description, str):
            raise ValueError(f"Regression Description is invalid: {str(self.description)}")
        
        # Make sure the lookback was extracted
        if not isinstance(self.lookback, int):
            raise ValueError(f"Regression Lookback is invalid: {str(self.lookback)}")

        # Make sure the predictions were extracted
        if not isinstance(self.predictions, int):
            raise ValueError(f"Regression Predictions is invalid: {str(self.predictions)}")

        # Set the Epoch's Seed on all required libraries
        seed(epoch_seed)
        npseed(epoch_seed)
        tf_random.set_seed(epoch_seed)











    #################
    ## Prediction  ##
    #################





    def predict(self, input_ds: ndarray) -> List[List[float]]:
        """Generates predictions based on the provided features.

        Args:
            input_ds: ndarray
                The dataset that will be used as input in order to generate
                predictions. Keep in mind that it is best to generate all 
                the predictions in one go.

        Returns:
            List[float]
        """
        # Generate the predictions
        preds: ndarray = self.model.predict_on_batch(input_ds)

        # Finally, return them in a list format
        return preds.tolist()[0]












    #############
    ## Feature ##
    #############





    def predict_feature(self, input_ds: ndarray) -> float:
        """Generates predictions based on the provided input dataset. Then, it converts
        them into features.

        Args:
            input_ds: ndarray
                The features dataset that will be used to generate predictions.

        Returns:
            float
        """
        # Firstly, predict the next trend
        preds: List[float] = self.predict(input_ds)

        # Finally, return the predicted feature
        return self._normalize_feature(Utils.get_percentage_change(input_ds[0, -1], preds[-1]))








    def _normalize_feature(self, predicted_change: float) -> float:
        """Given a predicted change, it will scale it to a range between
        -1 and 1 accordingly.

        Args:
            predicted_change: float
                The percentage change between the current price and the last
                predicted price.

        Returns:
            float
        """
        # Retrieve the adjusted change
        adjusted_change: float = self._calculate_adjusted_change(predicted_change)

        # Scale the increase change
        if adjusted_change > 0:
            return self._scale_feature(adjusted_change)
        
        # Scale the decrease change, keep in mind that the decrease data is in negative numbers.
        elif adjusted_change < 0:
            return -(self._scale_feature(-(adjusted_change)))
        
        # Otherwise, return 0 as a sign of neutrality
        else:
            return 0







    def _calculate_adjusted_change(self, change: float) -> float:
        """Adjusts the provided change to the min and max values in the
        regression discovery.

        Args:
            change: float
                The percentage change from the current price to the last 
                prediction.

        Returns:
            float
        """
        if change >= Regression.MIN_FEATURE_VALUE and change <= Regression.MAX_FEATURE_VALUE:
            return change
        elif change > Regression.MAX_FEATURE_VALUE:
            return Regression.MAX_FEATURE_VALUE
        elif change >= -(Regression.MAX_FEATURE_VALUE) and change <= -(Regression.MIN_FEATURE_VALUE):
            return change
        elif change < -(Regression.MAX_FEATURE_VALUE):
            return -(Regression.MAX_FEATURE_VALUE)
        else:
            return 0





    def _scale_feature(self, value: float) -> float:
        """Scales a prediction change based on the regression's min and max
        feature values

        Args:
            value: float
                The predicted price change that needs to be scaled.

        Returns: 
            float
        """
        return round(
            (value - Regression.MIN_FEATURE_VALUE) / (Regression.MAX_FEATURE_VALUE - Regression.MIN_FEATURE_VALUE), 
            6
        )