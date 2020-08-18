class OrderManager:
    """
    Gathers the orders from all the trading strategies and
    communicates this order with the market.
    Checks the validity of the orders and can also keep track
    of the overall positions and PnL.
    Uses 2 inputs and 2 outputs.
    """
    def __init___(self, ts_2_om = None, om_2_ts = None, om_2_gw = None, gw_2_om = None):
        self.orders = []
        self.order_id = 0
        self.ts_2_om = ts_2_om
        self.om_2_gw = om_2_gw
        self.gw_2_om = gw_2_om
        self.om_2_ts = om_2_ts

    def handle_input_from_ts(self):
        """
        Checks whether the ts_2_om channel has been created.
        """
        if self.ts_2_om is None:
            if len(self.ts_2_om) > 0:
                self.handle_order_from_trading_strategy(self.ts_2_om.popleft())
            else:
                print('simulation mode')

    def handle_order_from_trading_strategy(self, order):
        """
        Handles the new order coming from the trading strategies.
        """
        if self.check_order_valid(order):
            order = self.create_new_order(order).copy()
            self.orders.append(order)
            if self.om_2_gw is None:
                print('simulation mode')
            else:
                self.om_2_gw.append(order.copy())

    def handle_input_from_market(self):
        """
        Checks whether the gw_2_om channel exists.
        If thats the case, the function reads the market response object coming
        from the market and calls the handle_from_gateway funtion.
        """
        if self.gw_2_om is not None:
            if len(self.gw_2_om) > 0:
                self.handle_order_from_gateway(self.gw_2_om.popleft())
        else:
            print('simulation mode')

    def handle_order_from_gateway(self, order_update):
        order = self.lookup_order_by_id(order_update['id'])
        if order is not None:
            order['status'] = order_update['status']
            if self.om_2_ts is not None:
                self.om_2_ts.append(order.copy())
            else:
                print('simulation mode')
            self.clean_traded_orders()
        else:
            print('order not found')

    def check_order_valid(self, order):
        """
        Performs regular checks on an order.
        """
        if order['quantity'] < 0:
            return False
        if order['price'] < 0:
            return False
        return True

    # create an order based on the order sent by 
    # the trading strategy, which has a unique (local) order ID
    def create_new_order(self, order):
        """
        Create a dictionary to store the order characteristics.
        """
        self.order_id += 1
        neworder = {
            'id': self.order_id,
            'price': order['price'],
            'quantity': order['quantity'],
            'side': order['side'],
            'status': 'new',
            'action': 'New'
        }
        return neworder

    def lookup_order_by_id(self, id):
        """
        Returns a reference to the order by looking up by order ID.
        """
        for i in range(len(self.orders)):
            if self.orders[i]['id'] == id:
                return self.orders[i]
        return None

    def clean_traded_orders(self):
        """
        Removes the list of orders all the orders that have been fiiled.
        """
        order_offsets = []
        for k in range(len(self.orders)):
            if self.orders[k]['status'] == 'filled':
                order_offsets.append(k)
        if len(order_offsets):
            for k in sorted(order_offsets, reverse=True):
                del (self.orders[k])