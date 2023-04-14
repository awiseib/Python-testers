from ibapi.client import *
from ibapi.wrapper import *

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):

        mycontract = Contract()
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"    
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        self.reqContractDetails(orderId, mycontract)

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract)

        myorder = Order()
        myorder.orderId = reqId
        myorder.action = "SELL"
        myorder.tif = "GTC"
        myorder.orderType = "LMT"
        myorder.lmtPrice = 144.80
        myorder.totalQuantity = 10

        self.placeOrder(myorder.orderId, contractDetails.contract, myorder)


    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}")

    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"reqId: {reqId}, contract: {contract}, execution: {execution}")

app = TestApp()
app.connect("127.0.0.1", 7496, 100)
app.run()