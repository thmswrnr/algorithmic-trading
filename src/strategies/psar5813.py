from config import ALPACA_CONFIG
from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader
import pandas_ta as ta
import pandas as pd


class PSAR5813(Strategy):
    def initialize(self):
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        symbol = "AAPL"
        
        prices = self.get_historical_prices(symbol, 30, "day").df

        #prices = pd.DataFrame()
        #prices = prices.ta.ticker(symbol, period="2y", interval="1d")

        signal = self.generate_signal(prices)
        
        quantity = 100

        if signal == 'BUY':
            pos = self.get_position(symbol)
            if pos is not None:
                self.sell_all()

            order = self.create_order(symbol, quantity, "buy")
            self.submit_order(order)

        elif signal == 'SELL':
            pos = self.get_position(symbol)
            if pos is not None:
                self.sell_all()
                
            order = self.create_order(symbol, quantity, "sell")
            self.submit_order(order)

    def before_market_closes(self):
        self.sell_all()

    def generate_signal(self, prices):
        prices.columns = [c.lower() for c in prices.columns]

        prices.ta.ema(5, append=True)
        prices.ta.ema(8, append=True)
        prices.ta.ema(13, append=True)
        prices.ta.psar(append=True)

        #prices.columns = [c.lower() for c in prices.columns]

        prices['signal'] = None
        prices.loc[(prices.close >= prices.EMA_5) & (prices.EMA_5 >= prices.EMA_8) & (prices.EMA_8 >= prices.EMA_13) & (~prices['PSARl_0.02_0.2'].isna()), "signal"] = "BUY"
        prices.loc[(prices.close <= prices.EMA_5) & (prices.EMA_5 <= prices.EMA_8) & (prices.EMA_8 <= prices.EMA_13) & (~prices['PSARs_0.02_0.2'].isna()), "signal"] = "SELL"

        return prices['signal'][-1]

if __name__ == "__main__":
    trade = False
    if trade:
        broker = Alpaca(ALPACA_CONFIG)
        strategy = PSAR5813(broker=broker)
        bot = Trader()
        bot.add_strategy(strategy)
        bot.run_all()
    else:
        start = datetime(2021, 5, 22)
        end = datetime(2023, 5, 22)
        PSAR5813.backtest(
            YahooDataBacktesting,
            start,
            end
        )