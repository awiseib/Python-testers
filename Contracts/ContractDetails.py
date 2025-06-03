from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from ibapi.contract import ComboLeg
port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.rCount = 0

    def nextValidId(self, orderId: OrderId):
        mycontract = Contract()
        mycontract.symbol = "VWRA"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        # mycontract.currency = "GBP"

        self.reqContractDetails(reqId=orderId, contract=mycontract)
        
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        attrs = vars(contractDetails)
        print(
            datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "contractDetails.",
            f"reqId:{reqId}",
            "\n",
            "\n".join(f"{name}: {value}" for name, value in attrs.items())
        )
        
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

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)
        if errorString == "No security definition has been found for the request":
            self.disconnect()
        
app = TestApp()
app.connect("127.0.0.1", port, 0)
app.run()