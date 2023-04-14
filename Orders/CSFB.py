from decimal import Decimal
from ibapi.tag_value import TagValue
from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime
from ibapi.contract import *
from ibapi.order_state import *


port = 7496


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.exchange = "CSFBALGO"
        contract.currency = "USD"


        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "BUY"
        myorder.orderType = "MKT"
        # myorder.lmtPrice = 167.00
        myorder.totalQuantity = 1
        myorder.tif = "GTC"
        # myorder.whatIf = True

        # must be direct-routed to "CSFBALGO"
        myorder.algoStrategy = "GUERRILLA"
        myorder.algoParams = []
        myorder.algoParams.append(TagValue("StartTime", "12:30:00 US/Eastern"))
        myorder.algoParams.append(TagValue("EndTime", "16:00:00 US/Eastern"))
        myorder.algoParams.append(TagValue("ExecStyle", "Normal"))
        myorder.algoParams.append(TagValue("MinPercent", 10))
        myorder.algoParams.append(TagValue("MaxPercent", 20))
        myorder.algoParams.append(TagValue("DisplaySize", 100))
        # myorder.algoParams.append(TagValue("Auction", "Default"))
        myorder.algoParams.append(TagValue("BlockFinder", 0))
        myorder.algoParams.append(TagValue("BlockPrice", "388"))
        myorder.algoParams.append(TagValue("MinBlockSize", "150"))
        myorder.algoParams.append(TagValue("MaxBlockSize", "180"))
        myorder.algoParams.append(TagValue("IWouldPrice", "170"))
        
        self.placeOrder(myorder.orderId, contract, myorder)

    def openOrder(
        self,
        orderId: OrderId,
        contract: Contract,
        order: Order,
        orderState: OrderState,
    ):
        print(
            "openOrder.",
            f"orderId:{orderId}",
            f"contract:{contract}",
            f"order:{order}\n"
        )

    def orderStatus(
        self,
        orderId: OrderId,
        status: str,
        filled: Decimal,
        remaining: Decimal,
        avgFillPrice: float,
        permId: int,
        parentId: int,
        lastFillPrice: float,
        clientId: int,
        whyHeld: str,
        mktCapPrice: float,
    ):
        print(
            "orderStatus.",
            f"orderId:{orderId}",
            f"status:{status}",
            f"filled:{filled}",
            f"remaining:{remaining}",
            f"avgFillPrice:{avgFillPrice}",
            f"parentId:{parentId}",
            f"lastFillPrice:{lastFillPrice}",
        )

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"execDetails. reqId: {reqId}, contract: {contract}, execution: {execution}")


app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()

