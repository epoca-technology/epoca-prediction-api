[< Back](./README.md)


# PREDICTION API ERRORS


## Index (500000 - 500999)

500000: ``

500001: ``

500002: ``




## Candlestick (501000 - 501999)

501000: `The lookback df could not be built because there aren't enough candlesticks in the database. Needs: {limit}, Has: {len(candlesticks)}.`

501001: `The lookback df could not be retrieved because the candlesticks are out of sync. Needs: {min_timestamp}, Has: {candlesticks[-1]['ct']}"`

501002: ``

501003: ``

501004: ``




## Epoch (502000 - 502999)

502000: `Cannot predict because there isn't an active Epoch.`

502001: `The provided epoch id {epoch_id} is different to the current epoch {new_epoch['id']}.`

502002: ``

502003: ``






## Prediction Model (503000 - 503999)

503000: `The number of rows in the sma df does not match the regressions' lookback. Needs: {self.regression_lookback}, Has: {df.shape[0]}.`

503001: `The max price in the regression df {df['c'].max()} violates the highest amount permitted in the Epoch {self.highest_price_sma}.`

503002: `The min price in the regression df {df['c'].min()} violates the lowest value permitted in the Epoch {self.lowest_price_sma}.`

503003: ``