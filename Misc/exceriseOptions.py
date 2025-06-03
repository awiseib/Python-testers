from ibapi.client import *
from ibapi.wrapper import *

port = 7496
accountId = ""

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.contract_counter = 0
    def nextValidId(self, orderId: OrderId): 
        contract = Contract()
        contract.conId = 580482280
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"

        self.exerciseOptions(5003, contract, 1, 1, accountId, 1)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(orderId, contract, order, orderState)

    def error(
        self,
        reqId: TickerId,
        errorCode: int,
        errorString: str,
        advancedOrderRejectJson="",
    ):
        print(
            "error.",
            f"reqId:{reqId}",
            f"errorCode:{errorCode}",
            f"errorString:{errorString}",
            f"advancedOrderRejectJson:{advancedOrderRejectJson}",
        )
app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()