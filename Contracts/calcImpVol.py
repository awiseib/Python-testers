from ibapi.client import *
from ibapi.wrapper import *

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        mycontract.symbol = "SPX"
        mycontract.secType = "OPT"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        mycontract.lastTradeDateOrContractMonth = 20250602
        mycontract.right = "P"
        mycontract.strike = 5550

        self.calculateImpliedVolatility(orderId, mycontract, 86.52, 5560.12, [])
        
    def tickOptionComputation(self, reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        print(
            f"Option Price: {optPrice:.2f}\n",
            f"Implied Volatility: {(impliedVol*100):.3f}"
        )
    
    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        # if reqId != -1:
            print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        
app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()