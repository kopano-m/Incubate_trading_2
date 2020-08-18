import unittest
from OrderManager import OrderManager

class TestOrderBook(unittest.TestCase):
    
    def setUp(self):
        self.order_manager = OrderManager()

    def test_receive_order_from_trading_strategy(self):
        """
        Verifies whether an order is correctly received by the order manager.
        """
        order1 = {
            'id': 10,
            'price': 219,
            'quantity': 10,
            'side': 'bid',
        }
        self.order_manager.handle_order_from_trading_strategy(order1)
        self.assertEqual(len(self.order_manager.orders),1)
        self.order_manager.handle_order_from_trading_strategy(order1)
        self.assertEqual(len(self.order_manager.orders),2)
        self.assertEqual(self.order_manager.orders[0]['id'],1)
        self.assertEqual(self.order_manager.orders[1]['id'],2)

    def test_receive_order_from_trading_strategy_error(self):
        """
        Checks whether an order created with a negative price is rejected
        to prevent a malformed order from being sent to the market.
        """
        order1 = {
            'id': 10,
            'price': -219,
            'quantity': 10,
            'side': 'bid',
        }
        self.order_manager.handle_order_from_trading_strategy(order1)
        self.assertEqual(len(self.order_manager.orders),0)

    def test_receive_from_gateway_filled(self):
        """
        Confirms a market response has been propagated by the order manager.
        """
        self.test_receive_order_from_trading_strategy()
        orderexecution1 = {
            'id': 2,
            'price': 13,
            'quantity': 10,
            'side': 'bid',
            'status': 'filled'
        }
        # self.display_orders()
        self.order_manager.handle_order_from_gateway(orderexecution1)
        self.assertEqual(len(self.order_manager.orders), 1)

    def test_receive_from_gateway_acked(self):
        self.test_receive_order_from_trading_strategy()
        orderexecution1 = {
            'id': 2,
            'price': 13,
            'quantity': 10,
            'side': 'bid',
            'status' : 'acked'
        }
        # self.display_orders()
        self.order_manager.handle_order_from_gateway(orderexecution1)
        self.assertEqual(len(self.order_manager.orders), 2)
        self.assertEqual(self.order_manager.orders[1]['status'], 'acked')

    def display_orders(self):
        for o in self.order_manager.orders:
            print(o)
