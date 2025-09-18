import abc
import random
import datetime

class TradeExecutionStrategy(abc.ABC):
    @abc.abstractmethod
    def execute_trade(self, symbol, quantity, price=None):
        pass

class MarketOrderStrategy(TradeExecutionStrategy):
    def execute_trade(self, symbol, quantity, price=None):
        simulated_price = random.uniform(99.0, 101.0)
        total_value = simulated_price * quantity
        print(f"--- MARKET ORDER ---")
        print(f"Executing {quantity} shares of {symbol} at market price (${simulated_price:.2f}/share).")
        print(f"Total trade value: ${total_value:.2f}")
        return {"status": "Executed", "price": simulated_price, "value": total_value, "type": "Market"}

class LimitOrderStrategy(TradeExecutionStrategy):
    def __init__(self, limit_price):
        self._limit_price = limit_price

    def execute_trade(self, symbol, quantity, price=None):
        simulated_current_price = random.uniform(98.0, 102.0)
        print(f"--- LIMIT ORDER ---")
        print(f"Attempting to buy {quantity} shares of {symbol} at limit price ${self._limit_price:.2f} (Current market: ${simulated_current_price:.2f}).")
        if simulated_current_price <= self._limit_price:
            total_value = self._limit_price * quantity
            print(f"Limit order filled! Executed at ${self._limit_price:.2f}/share. Total value: ${total_value:.2f}")
            return {"status": "Filled", "price": self._limit_price, "value": total_value, "type": "Limit"}
        else:
            print(f"Limit order not filled. Market price ${simulated_current_price:.2f} is above limit ${self._limit_price:.2f}.")
            return {"status": "Pending", "price": None, "value": 0, "type": "Limit"}

class StopLossOrderStrategy(TradeExecutionStrategy):
    def __init__(self, stop_price):
        self._stop_price = stop_price

    def execute_trade(self, symbol, quantity, price=None):
        simulated_current_price = random.uniform(90.0, 110.0)
        print(f"--- STOP-LOSS ORDER ---")
        print(f"Monitoring {symbol} for stop price ${self._stop_price:.2f} (Current market: ${simulated_current_price:.2f}).")
        if simulated_current_price <= self._stop_price:
            execution_price = simulated_current_price * random.uniform(0.98, 1.0)
            total_value = execution_price * quantity
            print(f"Stop-loss triggered! Selling {quantity} shares of {symbol} at ${execution_price:.2f}/share. Total value: ${total_value:.2f}")
            return {"status": "Triggered & Executed", "price": execution_price, "value": total_value, "type": "Stop-Loss"}
        else:
            print(f"Stop-loss not triggered. Market price ${simulated_current_price:.2f} is above stop ${self._stop_price:.2f}.")
            return {"status": "Pending", "price": None, "value": 0, "type": "Stop-Loss"}

class TradingBot:
    def __init__(self, broker_id, execution_strategy: TradeExecutionStrategy):
        self._broker_id = broker_id
        self._execution_strategy = execution_strategy
        self._trade_history = []

    def set_execution_strategy(self, strategy: TradeExecutionStrategy):
        self._execution_strategy = strategy

    def place_order(self, symbol, quantity, price=None):
        print(f"\nTrading Bot '{self._broker_id}' placing order for {symbol}...")
        result = self._execution_strategy.execute_trade(symbol, quantity, price)
        self._trade_history.append({"timestamp": datetime.datetime.now(), "symbol": symbol, "quantity": quantity, "result": result})
        return result

    def get_trade_history(self):
        print("\n--- Trade History ---")
        for trade in self._trade_history:
            print(f"{trade['timestamp'].strftime('%H:%M:%S')} - {trade['symbol']} ({trade['quantity']}): {trade['result']['status']} @ ${trade['result'].get('price', 'N/A'):.2f} (Type: {trade['result']['type']})")

if __name__ == "__main__":
    bot = TradingBot("AlphaTrader", MarketOrderStrategy())

    bot.place_order("AAPL", 10, None)
    bot.place_order("GOOG", 5, None)

    bot.set_execution_strategy(LimitOrderStrategy(limit_price=99.50))
    bot.place_order("MSFT", 20)
    bot.place_order("MSFT", 20)

    bot.set_execution_strategy(LimitOrderStrategy(limit_price=100.50))
    bot.place_order("AMZN", 15)

    bot.set_execution_strategy(StopLossOrderStrategy(stop_price=95.00))
    bot.place_order("TSLA", 8)
    bot.place_order("TSLA", 8)

    bot.get_trade_history()