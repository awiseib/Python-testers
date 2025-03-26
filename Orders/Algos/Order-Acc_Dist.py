from ibapi.tag_value import TagValue
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import ComboLeg

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol = "ES"
        mycontract.secType = "BAG"
        mycontract.currency = "USD"
        mycontract.exchange = "SMART"

        leg1 = ComboLeg()
        leg1.conId = 495512552
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "CME"

        leg2 = ComboLeg()
        leg2.conId = 551601561
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "CME"

        mycontract.comboLegs = []
        mycontract.comboLegs.append(leg1)
        mycontract.comboLegs.append(leg2)
        
        myorder = Order()
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.lmtPrice = 100
        myorder.totalQuantity = 50
        # myorder.outsideRth = True
        # myorder.goodAfterTime = "20231128-16:30:00"
        myorder.algoStrategy = "AccuDistr"
        myorder.algoParams = []
        myorder.algoParams.append(TagValue("componentSize", 5))
        myorder.algoParams.append(TagValue("timeBetweenOrders", 30))
        myorder.algoParams.append(TagValue("randomizeTime20", int(0)))
        myorder.algoParams.append(TagValue("randomizeSize55", int(0)))
        # myorder.algoParams.append(TagValue("giveUp", 1))
        myorder.algoParams.append(TagValue("catchUp", int(1)))
        myorder.algoParams.append(TagValue("waitForFill", int(0)))
        myorder.algoParams.append(TagValue("activeTimeStart", "20:30:00 US/Eastern"))
        myorder.algoParams.append(TagValue("activeTimeEnd", "21:35:00 US/Eastern"))

        self.placeOrder(orderId, mycontract, myorder)

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
