from ibapi.client import *
from ibapi.wrapper import *
from ibapi.account_summary_tags import *

import threading
import time


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        self.reqAccountUpdatesMulti(orderId, "DU74649", "", False)
        
    def updatePortfolio(
        self,
        contract: Contract,
        position: Decimal,
        marketPrice: float,
        marketValue: float,
        averageCost: float,
        unrealizedPNL: float,
        realizedPNL: float,
        accountName: str,
    ):
        print(
            "updatePortfolio.",
            f"contract {contract}",
            f"position {position}",
            f"marketPrice {marketPrice}",
            f"marketValue {marketValue}",
            f"averageCost {averageCost}",
            f"unrealizedPNL {unrealizedPNL}",
            f"realizedPNL {realizedPNL}",
            f"accountName {accountName}",
        )

    def updateAccountValue(
        self, key: str, val: str, currency: str, accountName: str
    ):
        print("updateAccountValue.", key, val, currency, accountName)

    def updateAccountTime(self, timeStamp: str):
        print("updateAccountTime.", timeStamp)

    def updatePortfolio(self, contract: Contract, position: Decimal, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        print(f"updatePortfolio. contract: {contract.symbol}@{contract.exchange}:{contract.secType}, position: {position}, marketPrice: {marketPrice}, marketValue: {marketValue}, averageCost: {averageCost}, unrealizedPNL: {unrealizedPNL}, realizedPNL: {realizedPNL}")

    def accountDownloadEnd(self, accountName: str):
        print("accountDownloadEnd.", accountName)
        self.disconnect()

app = TestApp()
app.connect("127.0.0.1", 7496, 1001)
app.run()
