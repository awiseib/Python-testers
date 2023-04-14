from decimal import Decimal
from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from ibapi.contract import ComboLeg
from threading import Thread
import time

port = 7496

FUTCONTRACT = []

# request a list of contracts
class contractApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    # Build EClient parameters and Contract Details requests to be sent out
    def nextValidId(self, orderId: OrderId):
        strike = 3950

        while strike <= 4095:
            mycontract = Contract()

            mycontract.symbol = "ES"
            mycontract.secType = "FOP"
            mycontract.exchange = "CME"
            mycontract.currency = "USD"

            mycontract.lastTradeDateOrContractMonth = 20230317
            mycontract.right = "C"
            mycontract.strike = strike

            newThread = Thread(target=self.reqContractDetails(reqId=strike, contract=mycontract), daemon=True)
            strike += 5
            time.sleep(0.1)
        
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        FUTCONTRACT.append(contractDetails.contract)
        

    def contractDetailsEnd(self, reqId: int):
        print(f"total Contracts: {len(FUTCONTRACT)}")
        if reqId == 4095:
            self.disconnect()

# request market data for that list
class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.contract_counter = 0

    # Build EClient parameters and Contract Details requests to be sent out
    def nextValidId(self, orderId: OrderId):
            
        currentConId = 0
        nextConId = 1
        requestId = 123
        print("LOOP START")
        
        self.reqMarketDataType(4)
        for contract in range(len(FUTCONTRACT)):
            
            if nextConId < len(FUTCONTRACT):
                
                mycontract = FUTCONTRACT[currentConId]
                newThread = Thread(target=self.reqMktData(
                    reqId=int(mycontract.strike),
                    contract=mycontract,
                    genericTickList="",
                    snapshot=True,
                    regulatorySnapshot=False,
                    mktDataOptions=[],
                ), daemon=True)

                newThread.start()

                requestId += 1
                currentConId += 1
                nextConId += 1
                time.sleep(1)


    def tickPrice(
        self,
        reqId: TickerId,
        tickType: TickType,
        price: float,
        attrib: TickAttrib,
    ):
        print(
            "tickPrice.",
            f"reqId:{reqId}",
            f"tickType:{tickType}",
            f"price:{price}",
            f"attrib:{attrib}"
        )


def main():

    app = contractApp()
    app.connect("127.0.0.1", port, 1001)
    app.run()

    time.sleep(7)

    app = TestApp()
    app.connect("127.0.0.1", port, 1002)
    app.run()

if __name__ == "__main__":
    main()