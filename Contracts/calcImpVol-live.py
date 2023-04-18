from ibapi.client import *
from ibapi.wrapper import *
from ibapi.ticktype import TickTypeEnum
import threading
import time

port = 7496

PRICES = {1:0, 2:0, 3:0}

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        
    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        if TickTypeEnum.to_str(tickType) == "BID" and reqId == 2:
            PRICES[reqId] = price
        elif TickTypeEnum.to_str(tickType) == "LAST" and reqId == 1:
            PRICES[reqId] = price

    
    def tickOptionComputation(self, reqId: TickerId, tickType: TickType, tickAttrib: int, impliedVol: float, delta: float, optPrice: float, pvDividend: float, gamma: float, vega: float, theta: float, undPrice: float):
        if TickTypeEnum.to_str(tickType) =="CUST_OPTION_COMPUTATION":
            print(f"reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, impliedVol: {(impliedVol*100):.2f}%, derivPrice: {optPrice}, underPrice: {undPrice}")
        


underlying = Contract()
underlying.symbol = "SPY"
underlying.secType = "STK"
underlying.exchange = "SMART"
underlying.currency = "USD"


derivative = Contract()
derivative.symbol = "SPY"
derivative.secType = "OPT"
derivative.exchange = "SMART"
derivative.currency = "USD"
derivative.lastTradeDateOrContractMonth = 20230421
derivative.right = "C"
derivative.strike = 415



app = TestApp()
app.connect("127.0.0.1", port, 1001)
time.sleep(3)
threading.Thread(target=app.run).start()

app.reqMktData(1, underlying, "", False, False, [])
app.reqMktData(2, derivative, "", False, False, [])

underPrice = PRICES[1]
derivPrice = PRICES[2]
reqId = 3
while True:
    if PRICES[1] != underPrice:
        underPrice = PRICES[1]
        app.calculateImpliedVolatility(reqId, derivative, derivPrice, underPrice, [])
        reqId+=1
        
    if PRICES[2] != derivPrice:
        derivPrice = PRICES[2]
        app.calculateImpliedVolatility(reqId, derivative, derivPrice, underPrice, [])
        reqId+= 1
