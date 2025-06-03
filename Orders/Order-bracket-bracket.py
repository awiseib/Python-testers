from ibapi.client import *
from ibapi.wrapper import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        mycontract = Contract()
        mycontract.conId = 265598
        mycontract.exchange = "SMART"

        parent_price = 232.50
        parent_action = "BUY"
        quantity = 10.0

        parent = Order()
        parent.orderId = orderId
        parent.action = parent_action
        parent.orderType = "MKT"
        parent.totalQuantity = quantity
        # parent.outsideRth = True
        # parent.lmtPrice = parent_price
        parent.transmit = False

        profit_taker = Order()
        profit_taker.orderId = parent.orderId + 1
        profit_taker.parentId = parent.orderId
        profit_taker.action = "SELL" if parent_action == "BUY" else "BUY"
        profit_taker.orderType = "LMT"
        profit_taker.totalQuantity = quantity
        profit_taker.lmtPrice = parent_price + 5
        # profit_taker.lmtPrice = 140
        # profit_taker.outsideRth = True
        profit_taker.transmit = False

        profit_taker_taker = Order()
        profit_taker_taker.orderId = parent.orderId + 3
        profit_taker_taker.parentId = parent.orderId + 1
        profit_taker_taker.action = "BUY"
        profit_taker_taker.orderType = "LMT"
        profit_taker_taker.totalQuantity = quantity
        profit_taker_taker.lmtPrice = parent_price + 6
        # profit_taker.lmtPrice = 140
        # profit_taker.outsideRth = True
        profit_taker_taker.transmit = False

        stop_loss = Order()
        stop_loss.orderId = parent.orderId + 2
        stop_loss.parentId = parent.orderId
        stop_loss.action = "SELL" if parent_action == "BUY" else "BUY"
        stop_loss.orderType = "STP"
        stop_loss.totalQuantity = quantity
        stop_loss.auxPrice = parent_price - 5
        # stop_loss.auxPrice = 135.18
        # stop_loss.outsideRth = True
        stop_loss.transmit = False

        stop_loss_loss = Order()
        stop_loss_loss.orderId = parent.orderId + 4
        stop_loss_loss.parentId = parent.orderId + 2
        stop_loss_loss.action = "BUY"
        stop_loss_loss.orderType = "STP"
        stop_loss_loss.totalQuantity = quantity
        stop_loss_loss.auxPrice = parent_price - 6
        # stop_loss.auxPrice = 135.18
        # stop_loss.outsideRth = True
        stop_loss_loss.transmit = True

        self.placeOrder(parent.orderId, mycontract, parent)
        self.placeOrder(profit_taker.orderId, mycontract, profit_taker)
        self.placeOrder(stop_loss.orderId, mycontract, stop_loss)
        self.placeOrder(profit_taker_taker.orderId, mycontract, profit_taker_taker)
        self.placeOrder(stop_loss_loss.orderId, mycontract, stop_loss_loss)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}, orderState: {orderState.status}, submitter: {order.submitter}") 

    def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
            
app = TestApp()
app.connect("127.0.0.1", 7496, 1001)
app.run()
