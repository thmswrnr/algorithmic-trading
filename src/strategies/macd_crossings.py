from config import ALPACA_CONFIG
from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader
import pandas_ta as ta
import pandas as pd


class MACDCrossing(Strategy):

    def initialize(self):
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        symbol = "AAPL"
        ema_fast = 12
        ema_slow = 26
        ema_signal = 9
        
        prices = self.get_historical_prices(symbol, 200, "day").df

        #prices = pd.DataFrame()
        #prices = prices.ta.ticker(symbol, period="2y", interval="1d")

        signal = self.generate_signal(prices, ema_fast, ema_slow, ema_signal)

        quantity = 100

        if signal == 'BUY':
            pos = self.get_position(symbol)
            if pos is not None:
                self.sell_all()
            #current_price = self.get_last_price(symbol)
            #stop_loss = current_price*0.9
            #take_profit_loss = current_price*1.15
            #order = self.create_order(symbol, quantity, "buy", take_profit_price=take_profit_loss, stop_loss_price=stop_loss)
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

    def generate_signal(self, prices, ema_fast, ema_slow, ema_signal):
        prices.columns = [c.lower() for c in prices.columns]

        prices.ta.macd(close='close', fast=ema_fast, slow=ema_slow, signal=ema_signal, append=True)

        prices.columns = [c.lower() for c in prices.columns]

        signal = prices['macds_12_26_9']
        macd = prices['macd_12_26_9']

        if macd[-2] < signal[-2] and macd[-1] >= signal[-1]:
            return "BUY"
        
        elif macd[-2] > signal[-2] and macd[-1] <= signal[-1]:
            return "SELL"
        
        return None

if __name__ == "__main__":
    trade = False
    if trade:
        broker = Alpaca(ALPACA_CONFIG)
        strategy = MACDCrossing(broker=broker)
        bot = Trader()
        bot.add_strategy(strategy)
        bot.run_all()
    else:
        start = datetime(2021, 5, 22)
        end = datetime(2023, 5, 22)
        MACDCrossing.backtest(
            YahooDataBacktesting,
            start,
            end
        )