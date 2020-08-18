import unittest
from LiquidityProvider import LiquidityProvider
from TradingStrategy import TradingStrategy
from MarketSimulator import MarketSimulator
from OrderManager import OrderManager
from OrderBook import OrderBook
from collections import deque

class TestTradingSimulation(unittest.TestCase):
    """
    Creates the full trading system by gathering all the
    prior critical components together.
    Checks whether, for a given input, we have the expected
    output.
    Tests whether the PnL of the trading strategy has been
    updated accordingly.
    """
    def setUp(self):
        """
        Creates all the deques representing the communicaton
        channels within the trading system
        """
        self.lp_2_gateway = deque()
        self.ob_2_ts = deque()
        self.ts_2_om = deque()
        self.ms_2_om = deque()
        self.om_2_ts = deque()
        self.gw_2_om = deque()
        self.om_2_gw = deque()

        # Instantiate all critical components of trading system
        self.lp = LiquidityProvider(self.lp_2_gateway)
        self.ob = OrderBook(self.lp_2_gateway, self.ob_2_ts)
        self.ts = TradingStrategy(self.ob_2_ts, self.ts_2_om, self.om_2_ts)
        self.ms = MarketSimulator(self.om_2_gw, self.gw_2_om)
        self.om = OrderManager(self.ts_2_om, self.om_2_ts, self.om_2_gw, self.gw_2_om)

