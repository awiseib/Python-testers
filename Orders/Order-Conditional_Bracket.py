from ibapi.client import *
from ibapi.wrapper import *
import ibapi.order_condition as oc
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        mycontract.conId = 265598
        mycontract.exchange = "SMART"

        parent_action = "BUY"
        quantity = 10
        parent_price = 230

        parent = Order()
        parent.orderId = orderId
        parent.action = parent_action
        parent.orderType = "LMT"
        parent.totalQuantity = quantity
        parent.lmtPrice = parent_price
        parent.transmit = False
        parent.ocaGroup = "MAIN_GROUP3"
        parent.ocaType = 1
        parent.conditions = [
            oc.TimeCondition(
                isMore=True, 
                time="12:00:00 America/Chicago"
            )
          ]

        profit_taker = Order()
        profit_taker.orderId = parent.orderId + 1
        parent.ocaGroup = "MAIN_GROUP3"
        profit_taker.action = "SELL" if parent_action == "BUY" else "BUY"
        profit_taker.orderType = "LMT"
        profit_taker.totalQuantity = quantity
        profit_taker.lmtPrice = parent_price + 5
        profit_taker.transmit = False
        profit_taker.conditions = [
            oc.TimeCondition(
                isMore=True, 
                time="12:30:00 America/Chicago"
            )
          ]

        stop_loss = Order()
        stop_loss.orderId = parent.orderId + 2
        parent.ocaGroup = "MAIN_GROUP3"
        stop_loss.action = "SELL" if parent_action == "BUY" else "BUY"
        stop_loss.orderType = "STP"
        stop_loss.totalQuantity = quantity
        stop_loss.auxPrice = parent_price - 5
        stop_loss.transmit = True

        self.placeOrder(parent.orderId, mycontract, parent)
        self.placeOrder(profit_taker.orderId, mycontract, profit_taker)
        self.placeOrder(stop_loss.orderId, mycontract, stop_loss)


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
