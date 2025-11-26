from ibapi.client import *
from ibapi.wrapper import *
from ibapi.ticktype import TickTypeEnum
import time, threading

port=7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.contract = Contract()
        self.order = Order()
        self.oid = 0
        self.snapshotEnd = {}
        self.md = {}

    def nextValidId(self, orderId: OrderId):
        self.oid = orderId

    def nextOid(self):
        self.oid += 1
        return self.oid
    
    def tickPrice(self, reqId, tickType, price, attrib):
        if reqId not in self.md:
            self.md[reqId] = {}
        print(f"{TickTypeEnum.toStr(tickType)}:  {price}")
        self.md[reqId][TickTypeEnum.toStr(tickType)] = price

    def tickSnapshotEnd(self, reqId):
        self.snapshotEnd[reqId] = True
        print("ReqID Added to snapshotEnd.")

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}, orderState: {orderState.status}, Ref: {order.orderRef}")
        print(f"{orderId} || {self.oid}")
        if orderId == self.oid and orderState.status not in ["Filled", "Cancelled"]:
            self.contract = contract
            self.order = order

    def openOrderEnd(self):
        print("End of open orders.")
        if self.order.orderType == "LMT":
            self.reqMktData(self.order.orderId, self.contract, "", True, False, [])
            while self.order.orderId not in self.snapshotEnd:
                time.sleep(0.25)
            print("Order ID in snapshotEnd")
            self.order.lmtPrice = self.md[self.order.orderId]["OPEN"]
            self.order.totalQuantity = 100
            
            self.placeOrder(self.order.orderId, self.contract, self.order)
        else:
            print(f"{self.order.action} {self.contract.symbol} {self.order.totalQuantity}@{self.order.lmtPrice} STP: {self.order.trailStopPrice}, Offset: {self.order.trailingPercent}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        
if __name__ == "__main__":
    app = TestApp()
    app.connect("127.0.0.1", port, 1)
    time.sleep(1)
    threading.Thread(target=app.run).start()
    time.sleep(1)

    contract = Contract()
    contract.exchange = "SMART"
    contract.primaryExchange = "NASDAQ"
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.currency = "USD"
    
    order = Order()
    order.orderId = app.nextOid()
    order.action = "BUY"
    order.orderType = "LMT"
    order.lmtPrice = 200
    order.totalQuantity = 10
    
    app.placeOrder(order.orderId, contract, order)
    time.sleep(3)
    app.reqOpenOrders()