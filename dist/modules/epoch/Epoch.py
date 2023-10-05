from typing import Union, List
from gc import collect
from modules._types import IEpochRecord, IPrediction
from modules.utils.Utils import Utils
from modules.database.Database import TN, read_query
from modules.prediction_model.PredictionModel import PredictionModel




# Class
class Epoch:
    """Epoch Class

    This singleton manages the active epoch as well as the active instance 
    of the prediction model.

    Class Properties:
        MODEL: Union[PredictionModel, None]
            The instance of the active Prediction Model. If no Epoch is active,
            this value is None.
        GARBAGE_COLLECTION: Union[int, None]
        GARBAGE_COLLECTION_INTERVAL: int
            The time in which the garbage should be collected, as well as the
            interval. 
    """
    # Active Prediction Model
    MODEL: Union[PredictionModel, None] = None

    # The time in which the garbage collection should be executed
    GARBAGE_COLLECTION: Union[int, None] = None
    GARBAGE_COLLECTION_INTERVAL: int = 120 # 120 minutes




    @staticmethod
    def generate_prediction(
        epoch_id: str, 
        close_prices: List[float]
    ) -> IPrediction:
        """After ensuring the API is running the correct Epoch, it generates
        a prediction through the Prediction Model Instance.

        Args:
            epoch_id: str
                The ID of the active epoch.
            close_prices: List[float]
                The list of synced close prices that will be used to build the input ds.

        Returns:
            IPrediction

        Raises:
            RuntimeError:
                If the provided epoch id is invalid.
                If there isn't an active epoch or it cannot be retrieved from the db
                    for any reason.
                If the provided epoch id does not match the active one.
                If any of the Epoch Assets are not available in the directory.
        """
        # If the model has not been initialized or the Epoch ID doesnt match, 
        # retrieve the active epoch record so the model can be initialized.
        if Epoch.MODEL is None or Epoch.MODEL.epoch_id != epoch_id:
            # Retrieve the active epoch
            new_epoch: Union[IEpochRecord, None] = Epoch.get_active_epoch()

            # Make sure there is an active epoch
            if new_epoch is None:
                raise RuntimeError(Utils.api_error("Cannot predict because there isn't an active Epoch.", 502000))

            # Make sure the active Epoch matches the provided id
            if new_epoch["id"] != epoch_id:
                raise RuntimeError(
                    Utils.api_error(f"The provided epoch id {epoch_id} is different to the current epoch {new_epoch['id']}.", 502001)
                )
            
            # Initialize the instance of the model
            Epoch.MODEL = PredictionModel(new_epoch)

        # Generate the prediction
        pred: IPrediction = Epoch.MODEL.predict(close_prices)

        # If the garbage collector has not been set, do so
        if Epoch.GARBAGE_COLLECTION is None:
            Epoch.GARBAGE_COLLECTION = Utils.add_minutes(pred["t"], Epoch.GARBAGE_COLLECTION_INTERVAL)
        
        # Check if the garbage collector should be invoked
        elif Epoch.GARBAGE_COLLECTION <= pred["t"]:
            collect()
            Epoch.GARBAGE_COLLECTION = Utils.add_minutes(pred["t"], Epoch.GARBAGE_COLLECTION_INTERVAL)
        
        # Finally, return the prediction
        return pred










    @staticmethod
    def get_active_epoch() -> Union[IEpochRecord, None]:
        """Retrieves the record of the active Epoch. If there isnt an
        active one, it returns None instead.

        Returns:
            Union[IEpochRecord, None]
        """
        # Execute the query
        epoch_list: List[IEpochRecord] = read_query(f"SELECT * FROM {TN['epochs']} WHERE uninstalled IS NULL")

        # Return the epoch if any
        if len(epoch_list) == 1:
            return epoch_list[0]
        else:
            return None