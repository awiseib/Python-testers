from ibapi.client import *
from ibapi.wrapper import *


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        mycontract.symbol = "SPX"
        mycontract.secType = "OPT"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        mycontract.lastTradeDateOrContractMonth = "20270114"
        mycontract.right = "P"
        mycontract.strike = 7750

        self.calculateImpliedVolatility(
            reqId=orderId, 
            contract=mycontract, 
            optionPrice=175.52,  # Any value may be entered. Not all entered values may result in a calculated price.
            underPrice=7736.12, # Any value may be entered. Not all entered values may result in a calculated price.
            implVolOptions=[]
        )
        
    def tickOptionComputation(self, reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        '''
        When calculating price, greeks are returned as None type.
        '''
        print(
            f"Underlying Price: {undPrice:.2f}\n",
            f"Option Price: {optPrice:.2f}\n",
            f"Implied Volatility: {(impliedVol*100):.3f}"
        )

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        
app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()