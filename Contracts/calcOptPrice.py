from ibapi.client import *
from ibapi.wrapper import *
from ibapi.ticktype import TickTypeEnum

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        mycontract.symbol = "SPY"
        mycontract.secType = "OPT"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        mycontract.lastTradeDateOrContractMonth = 20250417
        mycontract.right = "P"
        mycontract.strike = 541

        self.calculateOptionPrice(orderId, mycontract, 0.299, 541.31, [])
        
    def tickOptionComputation(self, reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        print(
            f"Option Price: {optPrice:.2f}\n",
            f"Implied Volatility: {(impliedVol*100):.3f}\n",
            f"Delta: {delta:.3f}\n",
            f"Gamma: {gamma:.3f}\n",
            f"Vega: {vega:.3f}\n",
            f"Theta: {theta:.3f}"
        )
    
    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        if reqId != -1:
            print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()