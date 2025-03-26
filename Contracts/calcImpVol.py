from ibapi.client import *
from ibapi.wrapper import *
from ibapi.ticktype import TickTypeEnum

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        # mycontract.conId = 617579246

        mycontract.symbol = "SPY"
        mycontract.secType = "OPT"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        mycontract.lastTradeDateOrContractMonth = 20250417
        mycontract.right = "C"
        mycontract.strike = 415

        self.calculateImpliedVolatility(orderId, mycontract, 1.74, 414.09, [])
        
    def tickOptionComputation(self, reqId: TickerId, tickType: TickType, tickAttrib: int, impliedVol: float, delta: float, optPrice: float, pvDividend: float, gamma: float, vega: float, theta: float, undPrice: float):
        print(f"reqId: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, impliedVol: {(impliedVol*100):.2f}%, undPrice: {undPrice}")
        
    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()