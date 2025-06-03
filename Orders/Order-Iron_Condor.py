from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import ComboLeg

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        mycontract.symbol = "SPX"
        mycontract.secType = "BAG"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        firstBuy = ComboLeg()
        firstBuy.conId = 603761180 # SPX 3805 P
        firstBuy.action = "BUY"
        firstBuy.ratio = 1
        firstBuy.exchange = "SMART"

        firstSell = ComboLeg()
        firstSell.conId = 601920725 # SPX 3810 P
        firstSell.action = "SELL"
        firstSell.ratio = 1
        firstSell.exchange = "SMART"

        secondSell = ComboLeg()
        secondSell.conId = 601920554 # SPX 3825 C
        secondSell.action = "SELL"
        secondSell.ratio = 1
        secondSell.exchange = "SMART"

        secondBuy = ComboLeg()
        secondBuy.conId = 601920559 # SPX 3830 C
        secondBuy.action = "BUY"
        secondBuy.ratio = 1
        secondBuy.exchange = "SMART"

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.lmtPrice = -1.10
        myorder.totalQuantity = 1
        myorder.tif = "GTC"

        mycontract.comboLegs = []
        mycontract.comboLegs.append(firstBuy)
        mycontract.comboLegs.append(firstSell)
        mycontract.comboLegs.append(secondSell)
        mycontract.comboLegs.append(secondBuy)

        self.placeOrder(myorder.orderId, mycontract, myorder)

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
