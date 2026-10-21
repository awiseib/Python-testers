from ibapi.client import *
from ibapi.wrapper import *


class TestApp(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqAllOpenOrders() # This request provides TWS Orders to the API client.

        self.reqAutoOpenOrders( # This request binds future TWS orders to automatically return to this API client.
            bAutoBind=True      # Force new TWS order to be affiliated with this API ClientID (0).
        )

        self.reqOpenOrders()    # Request orders affiliated with this client ID. ClientID 0 will return TWS orders as well.

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"OpenOrders. Order ID: {orderId}, Contract: {contract}, Order: {order}, Order State: {orderState}")

    def orderStatus(self, orderId: int, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def openOrderEnd(self):
        print("End of open orders")
        self.disconnect()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")


app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()
