from decimal import Decimal
from ibapi.client import *
from ibapi.common import TickAttrib, TickerId
from ibapi.contract import Contract, ContractDetails, ComboLeg
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.ticktype import TickType
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

    # def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
    #     print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    # def completedOrder(self, contract: Contract, order: Order, orderState: OrderState):
    #     print(f"CompletedOrder. submitter: {order.submitter}")

    # def execDetails(self, reqId: int, contract: Contract, execution: Execution):
    #     print(f"reqId: {reqId}, contract: {contract}, execution: {execution}, submitter: {execution.submitter}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        
if __name__ == "__main__":
    contract = Contract()
    contract.conId = 265598
    contract.exchange = "SMART"

    order = Order()
    order.action = "BUY"
    order.orderType = "MKT"
    order.totalQuantity = 10
    app = TestApp()
    app.connect("127.0.0.1", port, 1)
    time.sleep(1)
    threading.Thread(target=app.run).start()
    time.sleep(1)

    app.placeOrder(app.nextOid(), contract, order)
    time.sleep(3)
    app.reqOpenOrders()