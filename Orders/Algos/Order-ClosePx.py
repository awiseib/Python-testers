from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue
from datetime import datetime

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.conId = 265598
        mycontract.exchange = "SMART"
        
        myorder = Order()
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.lmtPrice = 230
        myorder.totalQuantity = 50
        
        myorder.algoStrategy = "ClosePx"
        myorder.algoParams = []
        myorder.algoParams.append(TagValue("maxPctVol", 0.4))
        myorder.algoParams.append(TagValue("riskAversion", "Neutral")) # Mirrors TWS' "Urgency/Risk aversion" field.
        myorder.algoParams.append(TagValue("startTime", "20240709-06:06:49"))
        myorder.algoParams.append(TagValue("forceCompletion", int(True))) # Mirror's TWS' "Attempt completion by EOD" field.
        
        self.placeOrder(orderId, mycontract, myorder)

    def openOrder(self,orderId: OrderId,contract: Contract,order: Order,orderState: OrderState):
        print(f"{datetime.now().strftime('%H:%M:%S.%f')[:-3]} openOrder. orderId:{orderId}, contract:{contract}, order:{order}")

    def orderStatus(self, orderId: OrderId,status: str,filled: Decimal,remaining: Decimal,avgFillPrice: float,permId: int,parentId: int,lastFillPrice: float,clientId: int,whyHeld: str,mktCapPrice: float):
        print(f"{datetime.now().strftime('%H:%M:%S.%f')[:-3]},orderStatus. orderId:{orderId}, status:{status}, filled:{filled}, remaining:{remaining}, avgFillPrice:{avgFillPrice}, lastFillPrice:{lastFillPrice}")

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print("ERROR: ",errorCode, errorString)


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
