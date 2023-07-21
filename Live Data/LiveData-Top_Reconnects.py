from ibapi.client import *
from ibapi.wrapper import *
from ibapi.ticktype import TickTypeEnum
import time

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextOrderId = 0

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        mycontract.conId = 265598
        mycontract.exchange = "SMART"


        self.reqMktData(
            reqId=self.nextOrderId,
            contract=mycontract,
            genericTickList="",
            snapshot=False,
            regulatorySnapshot=False,
            mktDataOptions=[],
        )
        
    
    def tickPrice(
        self,
        reqId: TickerId,
        tickType: TickType,
        price: float,
        attrib: TickAttrib,
    ):
        print(
            "tickPrice.",
            f"reqId:{reqId}",
            f"tickType:{TickTypeEnum.to_str(tickType)}",
            f"price:{price}",
            f"attrib:{attrib}"
        )
        self.disconnect()
        time.sleep(2)
        mdStart()

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)

def mdStart():
    app = TestApp()
    app.connect("127.0.0.1", port, 1002)
    app.run()

if __name__ == "__main__":
    mdStart()