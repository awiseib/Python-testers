from decimal import Decimal
from ibapi.client import *
from ibapi.common import TickerId
from ibapi.wrapper import *

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
    
    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.conId = 265598
        mycontract.exchange = "SMART"
        # mycontract.conId = 9599491
        # mycontract.exchange = "SMART"
        
        self.reqMktDepth(
            reqId=orderId,
            contract=mycontract,
            numRows=100,
            isSmartDepth=True,
            mktDepthOptions=[]
        )

    def updateMktDepth(self, reqId: TickerId, position: TickerId, operation: TickerId, side: TickerId, price: float, size: Decimal):
        print(f"updateMktDepth. position: {position}, operation: {operation}, side: {'BID' if side == 1 else 'ASk'}, price: {price}, size: {size}")
        # self.cancelMktDepth(reqId, False)

    def updateMktDepthL2(self, reqId: TickerId, position: TickerId, marketMaker: str, operation: TickerId, side: TickerId, price: float, size: Decimal, isSmartDepth: bool):
        print(f"updateMktDepthL2 SmartRouted: {isSmartDepth}. position: {position}, marketMaker: {marketMaker}, operation: {operation}, side: {'BID' if side == 1 else 'ASK'}, price: {price}, size: {size}")
        # self.cancelMktDepth(reqId, isSmartDepth)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
