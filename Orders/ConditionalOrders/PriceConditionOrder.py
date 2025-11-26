from ibapi.client import *
from ibapi.wrapper import *
from ibapi.order_condition import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        mycontract = Contract()
        mycontract.conId = 731693973
        # mycontract.symbol = "SPY"
        # mycontract.secType = "STK"
        mycontract.exchange = "CME"
        # mycontract.currency = "USD"

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.orderType = "MKT"
        myorder.totalQuantity = 10
        myorder.tif = "DAY"

        oc = PriceCondition()
        oc.conId = 731693973
        oc.exchange = "CME"
        oc.isMore = True
        oc.price = 321.210
        '''
        Trigger Methods
        "Default",  # = 0,
        "DoubleBidAsk",  # = 1,
        "Last",  # = 2,
        "DoubleLast",  # = 3,
        "BidAsk",  # = 4,
        "LastBidAsk",  # = 7,
        "MidPoint" # = 8
        '''
        oc.triggerMethod = 0
        
        '''
        Conditions Cancel Order
        Set True if the condition should trigger the order's cancellation. 
        Set False if the condition should trigger the order's transmission.
        '''

        myorder.conditions = [oc]
        myorder.conditionsCancelOrder = False
        
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
