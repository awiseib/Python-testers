from decimal import Decimal
from ibapi.client import *
from ibapi.common import OrderId
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.wrapper import *
from ibapi.order_condition import *

port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        print(f"nextValidId. orderId={orderId}")

        mycontract = Contract()
        mycontract.symbol = "SPY"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.orderType = "MKT"
        myorder.totalQuantity = 10
        myorder.tif = "DAY"

        oc = ExecutionCondition()
        oc.symbol = "AAPL"
        oc.secType = "STK"
        oc.exchange = "SMART"
        
        '''
        Conditions Cancel Order
        Set True if the condition should trigger the order's cancellation. 
        Set False if the condition should trigger the order's transmission.
        '''
        myorder.conditionsCancelOrder = False
        myorder.conditions = [oc]
        
        self.placeOrder(orderId, mycontract, myorder)

    def openOrder(self, orderId: int, contract: Contract, order: Order, orderState: OrderState):
        print("openOrder.", orderId, contract, order, orderState)
    
    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: OrderId, parentId: OrderId, lastFillPrice: float, clientId: OrderId, whyHeld: str, mktCapPrice: float):
        print("orderStatus.", orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
