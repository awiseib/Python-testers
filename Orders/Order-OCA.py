from ibapi.client import *
from ibapi.wrapper import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        ### Leg for AAPL
        leg1_contract = Contract() 
        leg1_contract.conId = 265598
        leg1_contract.exchange = "SMART"

        leg1_order = Order()
        leg1_order.tif = "DAY"
        leg1_order.orderId = orderId
        leg1_order.action = "BUY"
        leg1_order.orderType = "LMT"
        leg1_order.lmtPrice = 235
        leg1_order.totalQuantity = 1
        leg1_order.ocaGroup = "TestOCA_", leg1_order.orderId
        leg1_order.ocaType = 1
        leg1_order.transmit = True

        app.placeOrder(leg1_order.orderId, leg1_contract, leg1_order)

        ## Leg for IBM
        leg2_contract = Contract() 
        leg2_contract.conId = 8314
        leg2_contract.exchange = "SMART"

        leg2_order = Order()
        leg2_order.tif = "GTC"
        leg2_order.orderId = orderId+1
        leg2_order.action = "SELL"
        leg2_order.orderType = "LMT"
        leg2_order.lmtPrice = 260
        leg2_order.totalQuantity = 1
        leg2_order.ocaGroup = "TestOCA_", leg1_order.orderId
        leg2_order.ocaType = 1
        leg2_order.transmit = True

        app.placeOrder(leg2_order.orderId, leg2_contract, leg2_order)

        ## Leg for KO
        leg3_contract = Contract() 
        leg3_contract.conId = 8894
        leg3_contract.exchange = "SMART"

        leg3_order = Order()
        leg3_order.tif = "GTC"
        leg3_order.orderId = orderId+2
        leg3_order.action = "BUY"
        leg3_order.orderType = "LMT"
        leg3_order.totalQuantity = 62
        leg3_order.lmtPrice = 10
        leg3_order.ocaGroup = "TestOCA_", leg1_order.orderId
        leg3_order.ocaType = 1
        leg3_order.transmit = True

        app.placeOrder(leg3_order.orderId, leg3_contract, leg3_order)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}, orderState: {orderState.status}, submitter: {order.submitter}") 

    def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
            
app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()