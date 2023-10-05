from typing import TypedDict, List, Literal, Dict, Union
from modules._types.regression_types import IRegressionConfig
from modules._types.discovery_types import IDiscovery





###################
## Configuration ##
###################



# Min Sum Function
# The prediction model's discovery calculates the means and the medians of the 
# successful predictions which then will be used to trade. For instance, If the 
# mean function is selected, the model will make use of the discovery's 
# increase_successful_mean and the decrease_successful_mean as the minimum sums
# in order to generate non-neutral predictions.
IMinSumFunction = Literal["mean", "median"]




# Regressions Per Model
# The number of regressions that are placed in the prediction model.
IRegressionsPerModel = Literal[4, 8, 16]





# Minified Configuration
# The minified configuration is used in order to narrow down the variations and
# identify which models lead to profitability.
class IPredictionModelMinifiedConfig(TypedDict):
    pcr: float              # Price Change Requirement
    msf: IMinSumFunction    # Min Sum Function
    msaf: float             # Min Sum Adjustment Factor
    ri: List[str]           # Regression IDs











############
## Assets ##
############





# Lookback Indexer
# The lookback indexer contains a dict with 1m candlestick open times as keys and 
# prediction candlestick indexes as values.
ILookbackIndexer = Dict[str, int]





# Test Dataset Labels
# A dict containing the list of labels (outcomes) within the test dataset. They are
# grouped by price change requirement in string format.
# It is also important to mention that they follow the adjusted prediction indexing
# and there may be less labels than features in some cases.
ITestDatasetLabel = Literal[1, -1]
ITestDatasetLabelKey = Literal["2.5", "3", "3.5", "4"]
ITestDatasetLabels = Dict[ITestDatasetLabelKey, List[ITestDatasetLabel]]





# Test Dataset Features
# A dict containing the list of features within the test dataset. They are grouped
# by regression ID and follow the adjusted prediction indexing.
ITestDatasetFeatures = Dict[str, List[float]]












#####################
## Prediction Dict ##
#####################




# Prediction Result
#  1 = Long
# -1 = Short
#  0 = Neutral
IPredictionResult = Literal[1, -1, 0]




# Prediction
# The final prediction dict generated by the model. It contains the result, the time
# in which the prediction was made and the list of features used to come to the result.
class IPrediction(TypedDict):
    # Prediction result: -1 | 0 | 1
    r: IPredictionResult # The Prediction API will always return this value as 0

    # The time in which the prediction was performed (milliseconds)
    t: int

    # The list of predicted features 
    f: List[float]

    # The sum of all the predicted features
    s: float














##############
## Backtest ##
##############




# Types of positions
IBacktestPositionType = Literal[1, -1] # 1 = long, -1 = short



# Backtest Position
# When a position is closed, it is saved in a list that can be reviewed in the GUI when
# the backtest completes.
class IBacktestPosition(TypedDict):
    # Type of position: 1 = long, -1 = short
    t: IBacktestPositionType

    # Prediction Dict
    p: IPrediction

    # Position Times
    ot: int                 # Open Timestamp
    ct: Union[int, None]    # Close Timestamp - Populated when the position is closed

    # Position Prices
    op: float   # Open Price
    tpp: float  # Take Profit Price
    slp: float  # Stop Loss Price

    # Close Price: This property is populated when a position is closed. It will
    # take value of the Take Profit Price or Stop Loss Price depending on the outcome.
    cp: Union[float, None]  
    
    # The outcome is populated once the position is closed. True for successful and False
    # for unsuccessful
    o: Union[bool, None]

    # Balance when the position is closed
    b: Union[float, None]




# Backtest Performance
# A dict containing all the information about the backtest executed on a model.
class IBacktestPerformance(TypedDict):
    # General
    position_size: float
    initial_balance: float
    final_balance: float
    profit: float
    fees: float
    leverage: float
    exchange_fee: float
    idle_minutes_on_position_close: int

    # Positions
    positions: List[IBacktestPosition]
    increase_num: int
    decrease_num: int
    increase_outcome_num: int
    decrease_outcome_num: int

    # Accuracy
    increase_accuracy: float
    decrease_accuracy: float
    accuracy: float

















######################
## Prediction Model ##
######################




# Prediction Model Configuration
# The configuration of the prediction model that is built for each profitable
# model config. This dict is exported and used to initialize the Model in the
# Prediction API.
class IPredictionModelConfig(TypedDict):
    # Identity of the Model.
    id: str

    # The price percentage change target
    price_change_requirement: float

    # Sum function used to determine the min increase and decrease sums
    min_sum_function: IMinSumFunction

    # The factor that is used to adjust the min sums
    min_sum_adjustment_factor: float

    # The minimum increase and decrease sums required to generate non-neutral predictions
    min_increase_sum: float
    min_decrease_sum: float

    # The list of regressions in the model
    regressions: List[IRegressionConfig]











#################
## Certificate ##
#################





# Prediction Model Certificate
# Once the profitable model configs are built, a certificate is issued
# for each one of them.
class IPredictionModelCertificate(TypedDict):
    # Identity of the Model.
    id: str

    # The date in which the model was created
    creation: int

    # The date range from the epoch that was used to build the prediction models
    test_ds_start: int
    test_ds_end: int

    # The configuration of the model
    model: IPredictionModelConfig

    # The discovery of the model
    discovery: IDiscovery

    # The backtest performance of the model
    backtest: IBacktestPerformance



    