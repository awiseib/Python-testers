from decimal import Decimal
from ibapi.client import *
from ibapi.common import TickerId
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.wrapper import *
import time, threading
port=7496

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
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}, orderState: {orderState.status}, Ref: {order.orderRef}")
        
    def openOrderEnd(self):
        print("End of open orders.")

    def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def completedOrder(self, contract: Contract, order: Order, orderState: OrderState):
        print(f"CompletedOrder. submitter: {order.submitter}")

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"reqId: {reqId}, contract: {contract}, execution: {execution}, submitter: {execution.submitter}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        
if __name__ == "__main__":
    app = TestApp()
    app.connect("127.0.0.1", port, 0)
    time.sleep(1)
    threading.Thread(target=app.run).start()
    time.sleep(1)

    contract = Contract()
    contract.conId = 265598 # Contract ID for AAPL Stock
    contract.exchange = "SMART"

    order = Order()
    order.orderId = app.nextOid()
    order.action = "BUY"
    order.orderType = "LMT"
    order.totalQuantity = 1.0
    order.lmtPrice = 256.0
    order.tif = "DAY"
    order.ptOrderType = "PRESET"
    order.ptOrderId = app.nextOid()
    order.slOrderType = "PRESET"
    order.slOrderId = app.nextOid()
    
    app.placeOrder(order.orderId, contract, order)

    