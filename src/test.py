from datetime import datetime

from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from .config import ALPACA_CONFIG


class MyStrategy(Strategy):
    # Custom parameters
    parameters = {
        "symbol": "SPY",
        "quantity": 1,
        "side": "buy"
    }

    def initialize(self, symbol=""):
        # Will make on_trading_iteration() run every 180 minutes
        self.sleeptime = "180M"

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        quantity = self.parameters["quantity"]
        side = self.parameters["side"]

        order = self.create_order(symbol, quantity, side)
        self.submit_order(order)


trader = Trader()
broker = Alpaca(ALPACA_CONFIG)
strategy = MyStrategy(
    broker=broker,
    parameters= {
        "symbol": "SPY"
    })

# Backtest this strategy
backtesting_start = datetime(2020, 1, 1)
backtesting_end = datetime(2020, 12, 31)
strategy.backtest(
    YahooDataBacktesting,
    backtesting_start,
    backtesting_end,
    # You can also pass in parameters to the backtesting class, this will override the parameters in the strategy
    parameters= {
        "symbol": "SPY"
    },
)

# Run the strategy live
trader.add_strategy(strategy)
trader.run_all()