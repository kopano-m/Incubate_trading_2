from random import randrange
from random import sample, seed

class LiquidityProvider:
    """
    Acts as a liquidity provider or exchange.
    It will send price updates tot he trading system.
    It will use the lp_2_gateway channel to send the price
    updates.
    """
    def __init__(self, lp_2_gateway=None):
        self.orders = []
        self.order_id = 0
        seed(0)
        self.lp_2_gateway = lp_2_gateway

    def lookup_orders(self, id):
        """
        Looks up orders in the list of orders.
        """
        count = 0
        for o in self.orders:
            if o['id'] == id:
                return o, count
            count += 1
        return None, None

    def insert_manual_order(self, order):
        """
        Inserts orders manually into the trading system.
        Will be used for unit testing some components.
        """
        if self.lp_2_gateway is None:
            print('simulation mode')
            return order
        self.lp_2_gateway.append(order.copy())

    def read_tick_data_from_data_source(self):
        SYMBOLS = ['AUDUSD=X', 'GBPUSD=X', 'CADUSD=X', 'CHFUSD=X', 'EURUSD=X', 'JPYUSD=X', 'NZDUSD=X']
        START_DATE = '2014-01-01'
        END_DATE = '2020-08-18'

        # DataSeries for each currency
        symbols_data = {}
        symbol = 'EURUSD=X'
        SRC_DATA_FILENAME = symbol + '_data.pkl'

        try:
            data = pd.read_pickle(SRC_DATA_FILENAME)
        except FileNotFoundError:
            data = data.DataReader(symbol, 'yahoo', START_DATE, END_DATE)
            data.to_pickle(SRC_DATA_FILENAME)

    def generate_random_order(self):
        """
        Randomly generates 3 types of orders:
        - New (will create a new order ID)
        - Modify (will  use the order ID of an order that
        created and will cjange the quantity)
        - Delete (will use the order ID and will delete 
        the order)
        Each time a new order is created the order ID is
        incremented.
        """
        price = randrange(8, 12)
        quantity = randrange(1, 10)*100
        side = sample(['buy', 'sell'], 1)[0]
        order_id = randrange(0, self.order_id+1)
        o = self.lookup_orders(order_id)

        new_order = False
        if o is None:
            action = 'new'
            new_order = True
        else:
            action = sample(['modify', 'delete'], 1)[0]

        ord = {
            'id': self.order_id,
            'price': price,
            'quantity': quantity,
            'side': side,
            'action': action
        }

        if not new_order:
            self.order_id += 1
            self.orders.append(ord)

        if not self.lp_2_gateway:
            print('simulation mode')
            return ord
        self.lp_2_gateway.append(ord.copy())
