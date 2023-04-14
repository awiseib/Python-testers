from ibapi.client import *
from ibapi.wrapper import *

port = 7496

class TestApp(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        self.reqCompletedOrders(apiOnly=False)

    def completedOrder(self, contract: Contract, order: Order, orderState: OrderState):
        print(contract, order, orderState)
        print("OrderID: ", order.orderId)


app = TestApp()
app.connect("127.0.0.1", port, 1007)
app.run()
