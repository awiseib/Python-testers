from ibapi.client import *
from ibapi.wrapper import *
from ibapi.ticktype import TickTypeEnum


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

        self.calculateOptionPrice(
            reqId=orderId, 
            contract=mycontract, 
            volatility=0.299, # Any value may be entered. Not all entered values may result in a calculated price.
            underPrice=541.31, # Any value may be entered. Not all entered values may result in a calculated price.
            optPrcOptions=[]
        )
        
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
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()