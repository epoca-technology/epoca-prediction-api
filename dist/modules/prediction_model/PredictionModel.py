from typing import List, Tuple
from numpy import ndarray, array
from pandas import DataFrame
from modules._types import IEpochRecord, IPredictionResult, IPrediction, IMinSumFunction
from modules.utils.Utils import Utils
from modules.regression.Regression import Regression






class PredictionModel:
    """PredictionModel Class

    This class handles the initialization and management of a Prediction Model, as well
    as the sub models.

    Class Properties:
        ...

    Instance Properties:
        Epoch:
            epoch_id: str
            sma_window_size: int
            highest_price_sma: float
            lowest_price_sma: float
            regression_lookback: int
            regression_predictions: int
        
        Model:
            id: str
            price_change_requirement: float
            min_sum_function: IMinSumFunction
            min_sum_adjustment_factor: float
            min_increase_sum: float
            min_decrease_sum: float
            regressions: List[Regression]
    """






    ####################
    ## Initialization ##
    ####################



    def __init__(self, epoch_record: IEpochRecord):
        """Initializes the Prediction Model Instance.

        Args:
            epoch_record: IEpochRecord
                The Epoch record containing all required data to initialize the
                model and submodels. Moreover, to generate predictions.

        Raises:
            ValueError:
                If there is an issue loading the regressions or any other features.
        """
        # Init the Epoch's ID
        self.epoch_id: str = epoch_record["config"]["id"]

        # Init the SMA Window Size
        self.sma_window_size: int = epoch_record["config"]["sma_window_size"]

        # Init the highest and lowest price simple moving average within the Epoch
        self.highest_price_sma: float = epoch_record["config"]["highest_price_sma"]
        self.lowest_price_sma: float = epoch_record["config"]["lowest_price_sma"]

        # Init the global regression properties
        self.regression_lookback: int = epoch_record["config"]["regression_lookback"]
        self.regression_predictions: int = epoch_record["config"]["regression_predictions"]

        # Init the Prediction Model's ID
        self.id: str = epoch_record["model"]["id"]

        # Init the model's target
        self.price_change_requirement: float = epoch_record["model"]["price_change_requirement"]

        # Init the model's min sum function
        self.min_sum_function: IMinSumFunction = epoch_record["model"]["min_sum_function"]

        # Init the model's min sum adjustment factor
        self.min_sum_adjustment_factor: float = epoch_record["model"]["min_sum_adjustment_factor"]

        # Init the min sum requirements
        self.min_increase_sum: float = epoch_record["model"]["min_increase_sum"]
        self.min_decrease_sum: float = epoch_record["model"]["min_decrease_sum"]

        # Init the regressions
        self.regressions: List[Regression] = [
            Regression(reg_config["id"], epoch_record["config"]["seed"]) for reg_config in epoch_record["model"]["regressions"]
        ]











    #################
    ## Prediction  ##
    #################





    def predict(self, close_prices: List[float]) -> IPrediction:
        """Generates a prediction based on the latest candlesticks.

        Args:
            close_prices: List[float]
                The list of synced close prices that will be used to build the input ds.

        Returns:
            IPrediction

        Raises:
            RuntimeError:
                If there is an issue of any kind when retrieving the prediction
                    candlesticks.
                If the min or max price sma in the lookback df violates the 
                    highest_price_sma or lowest_price_sma established in the
                    Epoch.
        """
        # Initialize the prediction result
        result: IPredictionResult = 0

        # Build the features
        features_sum, features = self._build_features(close_prices)
        
        # Finally, return the prediction
        return { "r": result, "t": Utils.get_time(), "f": features, "s": features_sum }














    ##############
    ## Features ##
    ##############






    def _build_features(self, close_prices: List[float]) -> Tuple[float, List[float]]:
        """Builds all the features that will be used by the prediction 
        model in order to generate predictions. It returns both, the
        list of features and the sum.

        Args:
            close_prices: List[float]
                The list of synced close prices that will be used to build the input ds.

        Returns:
            Tuple[float, List[float]]
            (features_sum, features)
        """
        # Make the input dataset for the regressions
        reg_input_ds: ndarray = self._make_regression_input_ds(close_prices)

        # Predict the regression features
        features: List[float] = [reg.predict_feature(reg_input_ds) for reg in self.regressions]

        # Finally, return the packed features
        return round(sum(features), 6), features






    


    def _make_regression_input_ds(self, close_prices: List[float]) -> ndarray:
        """Builds the input dataset that will be used to generate predictions
        with regressions.

        Args:
            close_prices: List[float]
                The list of synced close prices that will be used to build the input ds.

        Returns:
            ndarray

        Raises:
            RuntimeError:
                If the input dataset does not match the regressions' lookback.
                If the sma dataset contains prices that violates the highest_price_sma
                    or lowest_price_sma.
        """
        # Initialize the simple moving average df
        df: DataFrame = DataFrame({ "c": close_prices })
        df["c"] = df["c"].rolling(self.sma_window_size).mean()
        df.dropna(inplace=True)

        # Make sure the df contains the correct number of rows
        if df.shape[0] != self.regression_lookback:
            raise RuntimeError(Utils.api_error(f"The number of rows in the sma df does not \
                match the regressions' lookback. Needs: {self.regression_lookback}, Has: {df.shape[0]}.", 503000))

        # Ensure the sma prices within the df don't violate the min and max established by the epoch
        if df["c"].max() >= self.highest_price_sma:
            raise RuntimeError(Utils.api_error(f"The max price in the regression df {df['c'].max()} violates the \
                highest value permitted in the Epoch {self.highest_price_sma}.", 503001))
        elif df["c"].min() <= self.lowest_price_sma:
            raise RuntimeError(Utils.api_error(f"The min price in the regression df {df['c'].min()} violates the \
                lowest value permitted in the Epoch {self.lowest_price_sma}.", 503002))

        # Normalize the df
        df["c"] = df["c"].apply(lambda x: (x - self.lowest_price_sma) / (self.highest_price_sma - self.lowest_price_sma))

        # Build the dataset
        ds: ndarray = array([df["c"]])

        # Clear the df from RAM
        df = ""

        # Finally, return the input dataset
        return ds