from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue
from ibapi.contract import ComboLeg

port = 7497


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        mycontract.symbol = "AAPL,GOOG"
        mycontract.secType = "BAG"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        leg1 = ComboLeg()
        leg1.conId = 208813720
        leg1.exchange = "SMART"
        leg1.action = "BUY"
        leg1.ratio = 1

        leg2 = ComboLeg()
        leg2.conId = 265598
        leg2.exchange = "SMART"
        leg2.action = "SELL"
        leg2.ratio = 1
        

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.totalQuantity = 1
        myorder.tif = "DAY"
        mycontract.comboLegs = [leg2, leg1]

        myorder.lmtPrice = -80

        myorder.smartComboRoutingParams = []
        myorder.smartComboRoutingParams.append(TagValue("NonGuaranteed", "1"))


        self.placeOrder(myorder.orderId, mycontract, myorder)
        # self.reqOpenOrders()

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}, orderState: {orderState.status}, submitter: {order.submitter}") 

    def openOrderEnd(self):
        print("End of open orders")

    def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
            
app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
