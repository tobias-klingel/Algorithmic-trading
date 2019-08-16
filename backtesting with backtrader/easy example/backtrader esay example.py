import backtrader as bt
import backtrader.feeds as btfeeds

################################################################################################
# Read tick data
def input_tickData_csv(fileName):
    data = btfeeds.GenericCSVData(
        dataname=fileName,
        dtformat=('%Y-%m-%d'),
        datetime=0, high=2, low=3, open=1, close=4, volume=6,
    )
    return data
################################################################################################
# Strategy
class SMA_Strategy(bt.Strategy):

    # Initial setup of strategy
    def __init__(self):
        self.sma = bt.ind.SMA(period=30)
        sma1 = bt.ind.SMA(period=60)  # fast moving average
        sma2 = bt.ind.SMA(period=100)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    # Will be called for each tick (buy/sell decision)
    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long/buy

        elif self.crossover < 0:  # in the market & cross to the downside
            self.sell()  # Sell long position

######################################################
    # Information printing
    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_trade(self, trade):
        self.log('Operational profit, Gross %.2f, Net %.2f' %
                 (trade.pnl, trade.pnlcomm))
################################################################################################
#Main
if __name__ == '__main__':

    #############################################
    # Read data (tick data)
    data = input_tickData_csv('GDAXI.csv')

    #############################################
    # Setup backtesting
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SMA_Strategy)
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    beginningValue = cerebro.broker.getvalue()
    cerebro.broker.setcommission(commission=0.01)

    # Run backtesting
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()

    #############################################
    # Analyse results
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    pro = (cerebro.broker.getvalue() - beginningValue) / 100
    print("Profit: " + str(cerebro.broker.getvalue() - beginningValue) + " ; " + '%.2f'% pro)
    cerebro.plot(style='candlestick', barup='green', bardown='red')

