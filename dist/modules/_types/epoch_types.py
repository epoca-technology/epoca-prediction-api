from typing import TypedDict, Union
from modules._types.prediction_model_types import IPredictionModelConfig





# Epoch Config
# The configuration to be used by the Epoch and influence the entire infrastructure.
class IEpochConfig(TypedDict):
    # Random seed to be set on all required libraries in order to guarantee reproducibility
    seed: int

    # Identifier, must be preffixed with "_". For example: "_EPOCHNAME"
    id: str

    # Simple Moving Average Window Size
    # This value will be used when initializing the candlesticks. The normalized prediction
    # dataframe is built on these values rather than normal prices.
    sma_window_size: int

    # Train Split
    # This percent value is used to separate the data that is used to train and test the 
    # models. It is important to always evaluate models on data they have not yet seen.
    # It is also important to mention that this train split does not include the validation
    # data. Moreover, This value is also used to calculate the training_evaluation range.
    train_split: float

    # Validation Split
    # This percent value is used to separate the train data from the validation data in order
    # to be able to keep track of the model's progress during training.
    validation_split: float

    # The date range of the Epoch.
    start: int
    end: int

    # The date range of the test dataset (1 - train_split)
    test_ds_start: int
    test_ds_end: int

    # Highest and lowest price sma within the Epoch.
    # If the price was to go above the highest or below the lowest price, trading should be
    # stopped and a new epoch should be published once the market is "stable"
    highest_price_sma: float
    lowest_price_sma: float

    # Regression Parameters
    # The values that represent the input and the ouput of a regression.
    # The lookback stands for the number of candlesticks from the past it needs to look at
    # in order to generate a prediction.
    # The predictions stand for the number of predictions the regressions will generate.
    regression_lookback: int
    regression_predictions: int

    # Prediction Model Evaluation
    # exchange_fee: Two fees are charged per trade, one when the position is opened and then when 
    #   it is closed. Also keep in mind that the fees are charged based on the equity_size and not 
    #   the position_size.
    #   Binance 0.04% | Bitfinex 0.065% | Kucoin 0.06%
    # position_size: the total amount of USD that will be used when openning positions. The 
    #   total balance of the evaluation is equals to position_size * 2.
    # leverage: the leverage that will be used by the model evaluation to simulate real life
    #   trading.
    # idle_minutes_on_position_close: the number of minutes the prediction model will remain 
    # idle when a position is closed during the model evaluation.
    exchange_fee: float
    position_size: float
    leverage: int
    idle_minutes_on_position_close: int







# Default values to speed up the creation process
class IEpochDefaults(TypedDict):
    seed: int
    sma_window_size: int
    train_split: float
    validation_split: float
    epoch_width: int # Number of months that will comprise the Epoch
    regression_lookback: int
    regression_predictions: int
    exchange_fee: float
    position_size: float
    leverage: int
    idle_minutes_on_position_close: int








# Epoch Record
# The record of the epoch that is stored in the database and contains 
# all the neccessary information to initialize and operate the 
# Prediction Model.
class IEpochRecord(TypedDict):
    # The identifier of the epoch
    id: str

    # The date in which the epoch was installed
    installed: int

    # The full configuration of the epoch
    config: IEpochConfig

    # The configuration of the prediction model being exposed
    model: IPredictionModelConfig

    # The date in which the epoch was uninstalled. If this value is not set,
    # it means the epoch is still active.
    uninstalled: Union[int, None]
