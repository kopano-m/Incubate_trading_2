import backtrader as bt
import datetime


class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

        # Indicators for the plotting show
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
                                            subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

class Mltests(bt.Strategy):
    '''
    This strategy contains some additional methods that can be used to calcuate
    whether a position should be subject to a margin close out from Oanda.
    '''
    params = (('size', 100000),)

    def __init__(self):
        self.count = 0
        self.buybars = [1, 150]
        self.closebars = [100, 250]

    def next(self):
        bar = len(self.data)
        self.dt = self.data.datetime.date()
        if not self.position:
            if bar in self.buybars:
                self.cash_before = self.broker.getcash()
                value = self.broker.get_value()
                entry = self.buy(size=self.p.size)
                entry.addinfo(name='Entry')
        else:
            '''
            First check if margin close out conditions are met. If not, check
            to see if we should close the position through the strategy rules.

            If a close out occurs, we need to addinfo to the order so that we
            can log it properly later
            '''
            mco_result = self.check_mco(
                value=self.broker.get_value(),
                margin_used=self.margin
            )

            if mco_result == True:
                close = self.close()
                close.addinfo(name='MCO')

            elif bar in self.closebars:
                close = self.close()
                close.addinfo(name='Close')

        self.count += 1

    def notify_trade(self, trade):
        if trade.isclosed:
            print('{}: Trade closed '.format(self.dt))
            print('{}: PnL Gross {}, Net {}\n\n'.format(self.dt,
                                                round(trade.pnl,2),
                                                round(trade.pnlcomm,2)))

    def notify_order(self,order):
        if order.status == order.Completed:
            ep = order.executed.price
            es = order.executed.size
            tv = ep * es
            leverage = self.broker.getcommissioninfo(self.data).get_leverage()
            self.margin = abs((ep * es) / leverage)

            if 'name' in order.info:
                if order.info['name'] == 'Entry':
                    print('{}: Entry Order Completed '.format(self.dt))
                    print('{}: Order Executed Price: {}, Executed Size {}'.format(self.dt,ep,es,))
                    print('{}: Position Value: {} Margin Used: {}'.format(self.dt,tv,self.margin))
                elif order.info['name'] == 'MCO':
                    print('{}: WARNING: Margin Close Out'.format(self.dt))
                else:
                    print('{}: Close Order Completed'.format(self.dt))

    def check_mco(self, value, margin_used):
        '''
        Make a check to see if the margin close out value has fallen below half
        of the margin used, close the position.

        value: value of the portfolio for a given data. This is essentially the
        same as the margin close out value which is balance + pnl
        margin_used: Initial margin
        '''

        if value < (margin_used /2):
            return True
        else:
            return False


class OandaCSVData(bt.feeds.GenericCSVData):
    params = (
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%dT%H:%M:%S.%fZ'),
        ('datetime', 6),
        ('time', -1),
        ('open', 5),
        ('high', 3),
        ('low', 4),
        ('close', 1),
        ('volume', 7),
        ('openinterest', -1),
    )

