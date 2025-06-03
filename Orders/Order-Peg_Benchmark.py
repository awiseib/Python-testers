from ibapi.client import *
from ibapi.wrapper import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        mycontract.conId = 8314 # IBM STK
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        myorder = Order()
        myorder.orderId = orderId
        myorder.orderType = "PEG BENCH"
        # BUY or SELL
        myorder.action = "BUY"
        myorder.totalQuantity = 100
        #Beginning with price...
        myorder.startingPrice = 0
        #increase/decrease price..
        myorder.isPeggedChangeAmountDecrease = False
        #by... (and likewise for price moving in opposite direction)
        myorder.peggedChangeAmount = 3
        #whenever there is a price change of...
        myorder.referenceChangeAmount = 1
        #in the reference contract...
        myorder.referenceContractId = 265598 # IGF STK
        #being traded at...
        myorder.referenceExchangeId = "SMART"
        #starting reference price is...
        myorder.stockRefPrice = 230
        #Keep myorder active as long as reference contract trades between...
        myorder.stockRangeLower = 220
        #and...
        myorder.stockRangeUpper = 230

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

