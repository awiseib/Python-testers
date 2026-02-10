from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
import time, threading

lock = threading.Lock()
port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.validExchanges = {}

    def nextValidId(self, orderId: OrderId):
        self.oid = 0

    def nextValidId(self, orderId: OrderId):
        self.oid = orderId

    # Automate the order identifier system.
    def nextOid(self):
        self.oid += 1
        return self.oid
    
    # Monitor our orders. Feel free to implement EWrapper.openOrder and EWrapper.execDetails as well for more information.
    def orderStatus(self, orderId: TickerId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: TickerId, parentId: TickerId, lastFillPrice: float, clientId: TickerId, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        # This prints out our contracts and list of exchanges
        print(f"{contractDetails.contract}: {contractDetails.validExchanges}")

        # The ContractDetails.validExchanges value is a string with comma-separated exchanges inside.
        validExchanges = contractDetails.validExchanges.split(",")
        
        # Assign the contract and exchanges to a dictionary like {localSymbol: [Exchange1, Exchange2, ...] } 
        self.validExchanges[contractDetails.contract.localSymbol] = validExchanges
        
    def contractDetailsEnd(self, reqId: int):
        print(datetime.now().strftime("%H:%M:%S.%f")[:-3], "contractDetailsEnd.", f"reqId:{reqId}")
        lock.release()

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")
        
if __name__ == "__main__":

    # Create our EClient/EWrapper object and initialize the run loop.
    app = TestApp()
    app.connect("127.0.0.1", port, 0)
    time.sleep(1)
    threading.Thread(target=app.run).start()
    time.sleep(1)

    # Specify our contract details we'd like to begin trading. This is just a random AAPL contract that was chosen.
    contract = Contract()
    contract.symbol = "AAPL"
    contract.exchange = "SMART"
    contract.secType = "OPT"
    contract.currency = "USD"
    contract.strike = 285
    contract.right = "P"
    contract.lastTradeDateOrContractMonth = "20260320"
    
    # Lock our thread until we receive all contracts back based on our parameters.
    with lock:
        app.reqContractDetails(app.nextOid(), contract)
        lock.acquire()
    
    if len(app.validExchanges.keys()) > 0:
        # Create a generic order we'd like to test with.
        order = Order()
        order.action = "BUY"
        order.orderType = "MKT"
        order.tif = "DAY"
        order.totalQuantity = 1
        order.goodAfterTime = "20260211 09:30:00 US/Eastern"

        # Iterate through the contracts we'd like to test with.
        for con in app.validExchanges.keys():
            testCon = Contract()
            testCon.localSymbol = con
            testCon.secType = "OPT"
            
            # For each exchange affiliated with a contract, send an order. 
            for exch in app.validExchanges[con]:
                print(f"Placing order for {con}@{exch}")
                testCon.exchange = exch
                app.placeOrder(app.nextOid(), testCon, order)