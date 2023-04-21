from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from threading import Thread
import time
port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        
        mycontract = Contract()
        # mycontract.conId = 617579246
        mycontract.localSymbol = "ESU1"

        # mycontract.symbol = "DAX"
        mycontract.secType = "FUT"
        mycontract.exchange = "CME"
        mycontract.currency = "USD"
        mycontract.includeExpired = True

        # mycontract.lastTradeDateOrContractMonth = 20230321
        # mycontract.right = "P"
        # mycontract.strike = 3950
        # mycontract.primaryExchange = "NYSE"
        # mycontract.localSymbol = "CH3"
        # mycontract.tradingClass = "SPXW"

        self.reqContractDetails(reqId=orderId, contract=mycontract)
        
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        attrs = vars(contractDetails)
        contractDetails.contract.conId
        print(
            datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "contractDetails.",
            f"reqId:{reqId}",
            "\n",
            "\n".join(f"{name}: {value}" for name, value in attrs.items()),
            contractDetails.contract.conId
        )
        print(contractDetails.contract)
        
    def contractDetailsEnd(self, reqId: int):
        print(
            datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "contractDetailsEnd.",
            f"reqId:{reqId}",
        )
        self.disconnect()
        
    def bondContractDetails(self, reqId: int, contractDetails: ContractDetails):
        attrs = vars(contractDetails)
        print(
            datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "bondDetails.",
            f"reqId:{reqId}",
            "\n",
            "\n".join(f"{name}: {value}" for name, value in attrs.items()),
        )

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        return super().error(reqId, errorCode, errorString, advancedOrderRejectJson)
        
app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()