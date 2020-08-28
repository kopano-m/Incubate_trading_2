from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import os.path
import sys

import backtrader as bt

from strategies.tests import TestStrategy, Mltests, OandaCSVData

if __name__ == "__main__":
    tframes = dict(
        minutes=bt.TimeFrame.Minutes,
        daily=bt.TimeFrame.Days,
        weekly=bt.TimeFrame.Weeks,
        monthly=bt.TimeFrame.Months)
    cerebro = bt.Cerebro()

    #cerebro.addstrategy(TestStrategy)

    #modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #datapath = os.path.join(modpath, './data/EURUSD=X.csv')

    #data = bt.feeds.YahooFinanceCSVData(
     #   dataname=datapath,
      #  fromdate=datetime.datetime(2019,8,24),
       # todate=datetime.datetime(2020,8,25),
       # revere=False
    #)
        #Add our strategy
    cerebro.addstrategy(Mltests)

    #get oanda data
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, './data/EUR_USD-2005-2017-D1.csv')
    
    data = OandaCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2005, 1, 1),
        todate=datetime.datetime(2006, 1, 1))

    cerebro.adddata(data)

    cerebro.broker.setcash(100000.0)

    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set the commission - 0.1%
    # cerebro.broker.setcommission(commission=0.001)

    cerebro.broker.setcommission(leverage=50)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()
