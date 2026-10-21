import time
import threading
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.oid = 0

    def nextValidId(self, orderId: OrderId):
        self.oid = orderId

    def nextOid(self):
        self.oid += 1
        return self.oid


    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}, orderState: {orderState}")

    def openOrderEnd(self):
        print("End of open orders.")

    def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
        print("orderStatus.", orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"reqId: {reqId}, contract: {contract}, execution: {execution}, submitter: {execution.submitter}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        
if __name__ == "__main__":

    app = TestApp()
    app.connect(host="127.0.0.1", port=7497, clientId=0)
    time.sleep(1)
    threading.Thread(target=app.run).start()
    time.sleep(1)

    mycontract = Contract()
    mycontract.symbol = "AAPL"
    mycontract.secType = "STK"
    mycontract.exchange = "SMART"
    mycontract.currency = "USD"

    myorder = Order()
    myorder.action = "BUY"
    myorder.tif = "DAY"
    myorder.orderType = "MKT"
    myorder.totalQuantity = 7032
    myorder.algoStrategy = "Vwap"
    myorder.algoParams = [TagValue("endTime", "20261020-13:30:00")]
    app.placeOrder(app.nextOid(), mycontract, myorder)