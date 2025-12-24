from ibapi.client import *
from ibapi.wrapper import *

port = 7496
accountId = "U1234567"

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        
    def nextValidId(self, orderId: OrderId): 
        contract = Contract()
        contract.conId = 580482280
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"

        '''
        contract: Contract - This structure contains a description of the contract to be exercised
        exerciseAction:int - Specifies whether you want the option to lapse or be exercised.
            Values are 1 = exercise, 2 = lapse.
        exerciseQuantity:int - The quantity you want to exercise.
        account:str - destination account
        override:int - Specifies whether your setting will override the system's natural action. For example, if your action is "exercise" and the option is not in-the-money, by natural action the option would not exercise. If you have override set to "yes" the natural action would be overridden and the out-of-the money option would be exercised.
            Values are: 0 = no, 1 = yes.
        manualOrderTime:str - manual order time
        customerAccount:str - customer account
        professionalCustomer:bool - professional customer
        '''

        self.exerciseOptions(5003, contract, 1, 1, accountId, 1)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"OpenOrders. Order ID: {orderId}, Contract: {contract}, Order: {order}, Order State: {orderState}")

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)
        if errorString == "No security definition has been found for the request":
            self.disconnect()

app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()
