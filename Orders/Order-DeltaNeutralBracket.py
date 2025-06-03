from ibapi.client import *
from ibapi.wrapper import *
import time
port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        # contract for an AAPL call
        mycontract = Contract()
        mycontract.conId = 682695687
        mycontract.exchange = "SMART"

        # buying call with limit order
        parent = Order()
        parent.orderId = orderId
        parent.action = "BUY"
        parent.orderType = "LMT"
        parent.totalQuantity = 1
        parent.lmtPrice = 11.50
        parent.transmit = False # set to false to send with child

        # make a contract for AAPL stock for hedge
        hedge_contract = Contract()
        hedge_contract.conId = 756733
        hedge_contract.exchange = "SMART"
        '''
        Child order to sell stock, triggered by parent fill.
        Note that this is a LMT order with no limit price specified,
        which means the limit price will be taken from current best bid
        at the time of parent fill (or ask if buying). I don't think
        you can use a MKT order here when paired with parent LMT, but
        you could specify a different limit price to guarantee a fill.
        The hedged delta will be taken from the parent order option's 
        delta at time of order fill and used to generate an order quantity. 
        '''
        delta_hedge = Order()
        delta_hedge.action = "SELL"
        delta_hedge.orderType = "MKT"
        delta_hedge.orderId = orderId + 1
        delta_hedge.parentId = parent.orderId
        delta_hedge.hedgeType = "D"
        delta_hedge.totalQuantity = 0
        # delta_hedge.hedgeParam = "50"
        # delta_hedge.hedgeType = "D" # D for delta hedge
        # delta_hedge.hedgeParam = "delta=50"
        delta_hedge.dontUseAutoPriceForHedge = True
        delta_hedge.transmit = True # set to true to send whole "bracket"

        # send both orders, with child's transmit=True submitting both
        self.placeOrder(parent.orderId, mycontract, parent)
        time.sleep(1)
        self.placeOrder(delta_hedge.orderId, hedge_contract, delta_hedge)

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
