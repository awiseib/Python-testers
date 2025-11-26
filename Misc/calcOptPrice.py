from ibapi.client import *
from ibapi.wrapper import *
import threading,time,datetime

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.oid = 0
        self.roundTrip = {}
        self.cap = 1000

    def nextValidId(self, orderId: OrderId):
        self.oid = orderId

    def nextOid(self):
        self.oid += 1
        return self.oid
        
    def tickOptionComputation(self, reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        # print(
        #     f"Option Price: {optPrice:.2f}\n",
        #     f"Implied Volatility: {(impliedVol*100):.3f}\n",
        #     f"Delta: {delta:.3f}\n",
        #     f"Gamma: {gamma:.3f}\n",
        #     f"Vega: {vega:.3f}\n",
        #     f"Theta: {theta:.3f}"
        # )
        print(f"{reqId}: {(datetime.datetime.now()-self.roundTrip[reqId]['start']).seconds} seconds")
        if reqId == app.cap-1:
            print(f"Total Time: {(datetime.datetime.now()-self.roundTrip[0]['start']).seconds} seconds")

    
    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        # if reqId != -1:
            print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
  
app = TestApp()
app.connect("127.0.0.1", port, 0)
time.sleep(3)
threading.Thread(target=app.run).start()
time.sleep(1)
      
for i in range(0,app.cap):
    app.roundTrip[i] = {}
mycontract = Contract()
mycontract.symbol = "SPY"
mycontract.secType = "OPT"
mycontract.exchange = "SMART"
mycontract.currency = "USD"

mycontract.lastTradeDateOrContractMonth = 20250718
mycontract.right = "P"
mycontract.strike = 622

vol = 0.100
for i in range(0,app.cap):
    vol += (i/1000)
    app.roundTrip[i]["start"] = datetime.datetime.now()
    app.calculateOptionPrice(i, mycontract, vol, 624.15, [])
