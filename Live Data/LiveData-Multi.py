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
        
        mycontract = Contract()
        mycontract.symbol = "CL"
        mycontract.secType = "FUT"
        mycontract.exchange = "NYMEX"
        mycontract.currency = "USD"

        self.reqContractDetails(reqId=orderId, contract=mycontract)
        
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        FUTCONTRACT.append(contractDetails.contract)
        

    def contractDetailsEnd(self, reqId: int):
        print(f"total Contracts: {len(FUTCONTRACT)}")
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
        requestId = 100
        print("LOOP START")
        
        for contract in range(len(FUTCONTRACT)):
            
            if nextConId < len(FUTCONTRACT):
                
                
                mycontract = Contract()
                mycontract.symbol = "CL"
                mycontract.secType = "BAG"
                mycontract.exchange = "SMART"
                mycontract.currency = "USD"

                leg1= ComboLeg()
                leg1.conId = FUTCONTRACT[currentConId]
                leg1.ratio = 1
                leg1.action = "SELL"
                leg1.exchange = "NYMEX"

                leg2= ComboLeg()
                leg2.conId = FUTCONTRACT[nextConId]
                leg2.ratio = 1
                leg2.action = "BUY"
                leg2.exchange = "NYMEX"

                mycontract.comboLegs = []
                mycontract.comboLegs.append(leg1)
                mycontract.comboLegs.append(leg2)


                self.reqMktData(requestId,mycontract,"",False,False,[])

                requestId += 1
                currentConId += 1
                nextConId += 1


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

    # def tickSnapshotEnd(self, reqId: int):
    #     print(f"tickSnapshotEnd. reqId:{reqId}")


def main():

    app = contractApp()
    app.connect("127.0.0.1", port, 1001)
    app.run()

    time.sleep(3)

    app = TestApp()
    
    app.connect("127.0.0.1", port, 1002)
    app.run()

if __name__ == "__main__":
    main()