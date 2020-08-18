from random import randrange

class MarketSimulator:
    """
    Fixes the market assumptions.
    """
    def __init__(self, om_2_gw=None, gw_2_om=None):
        self.orders = []
        self.om_2_gw = om_2_gw
        self.gw_2_om = gw_2_om

    def lookup_orders(self, order):
        """
        Looks up outstanding orders.
        """
        count = 0
        for o in self.orders:
            if o['id'] == order['id']:
                return o, count
            count += 1
        return None, None

    def handle_order_from_gw(self):
        """
        Collects the order from the gateway (the om) through
        the om_2_gw channel.
        """
        if self.om_2_gw is not None:
            if len(self.om_2_gw) > 0:
                self.handle_order(self.om_2_gw.popleft())
        else:
            print('simulation mode')

    def handle_order(self, order):
        """
        Accepts any new order.
        If an order already has the same order ID, the order
        will be dropped. If the order manager cancels or
        amends an order, the order is automatically canceled
        and amended.
        """
        o, offset = self.lookup_orders(order)
        if o is None:
            if order['action'] == 'New':
                order['status'] = 'accepted'
                self.orders.append(order)
                if self.gw_2_om is not None:
                    self.gw_2_om.append(order.copy())
                else:
                    print('simulation mode')
                return
            elif order['action'] == 'Cancel' or order['action'] == 'Amend':
                print('Order id - not found - Rejection')
                if self.gw_2_om is not None:
                    self.gw_2_om.append(order.copy())
                else:
                    print('simulation mode')
                return
        elif o is not None:
            if order['action'] == 'New':
                print('Duplication order - Rejection')
                return
            elif order['action'] == 'Cancel':
                o['status'] = 'cancelled'
                if self.gw_2_om is not None:
                    self.gw_2_om.append(o.copy())
                else:
                    print('simulation mode')
                del (self.orders[offset])
                print('Order cancelled')
            elif order['action'] == 'Amend':
                o['status'] = 'accepted'
                if self.gw_2_om is not None:
                    self.gw_2_om.append(o.copy())
                else:
                    print('simulation mode')
                print('Order amended')

    def fill_all_orders(self, ratio=100):
        orders_to_be_removed = []
        for index, order in enumerate(self.orders):
            if randrange(100) <= ratio:
                order['status'] = 'filled'
            else:
                order['status'] = 'cancelled'
            orders_to_be_removed.append(index)
            if self.gw_2_om is not None:
                self.gw_2_om.append(order.copy())
            else:
                print('simulation mode')
        for i in sorted(orders_to_be_removed, reverse=True):
            del(self.orders[i])
