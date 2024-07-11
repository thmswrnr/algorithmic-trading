from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from strategies.trend import Trend
from strategies.swing_high import SwingHigh

def backtest():
    start = datetime(2022, 4, 15)
    end = datetime.now()
    result= Trend.backtest(
        YahooDataBacktesting,
        start,
        end
    )
    result.plot()


if __name__ == "__main__":
    backtest()
