import ccxt
import time
from security import load_secure_config  # Import the secure config loader

class CryptoBot:
    def __init__(self, config_file='secure_config.enc', exchange_id='binance'):
        config = load_secure_config(config_file)
        self.exchange = getattr(ccxt, exchange_id)({
            'apiKey': config['api_key'],
            'secret': config['api_secret'],
        })
        self.exchange.load_markets()

    def fetch_balance(self):
        try:
            return self.exchange.fetch_balance()
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None

    def fetch_ticker(self, symbol):
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as e:
            print(f"Error fetching ticker: {e}")
            return None

    def create_order(self, symbol, order_type, side, amount, price=None):
        try:
            if order_type == 'limit':
                return self.exchange.create_limit_order(symbol, side, amount, price)
            elif order_type == 'market':
                return self.exchange.create_market_order(symbol, side, amount)
            else:
                raise ValueError("Order type must be 'limit' or 'market'")
        except Exception as e:
            print(f"Error creating order: {e}")
            return None

    def run(self, symbol, amount, price):
        while True:
            ticker = self.fetch_ticker(symbol)
            if ticker:
                print(f"Current price of {symbol}: {ticker['last']}")
                if ticker['last'] < price:
                    print(f"Placing buy order for {amount} {symbol} at {price}")
                    order = self.create_order(symbol, 'limit', 'buy', amount, price)
                    if order:
                        print(f"Order placed: {order}")
            time.sleep(60)  # Add a delay to avoid excessive API calls

if __name__ == "__main__":
    bot = CryptoBot()
    symbol = 'BTC/USDT'
    amount = 0.001
    price = 30000  # Example price to buy
    bot.run(symbol, amount, price)