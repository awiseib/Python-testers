from ibapi.client import *
from ibapi.ticktype import TickType
from ibapi.utils import Decimal
from ibapi.wrapper import *
from threading import Thread
import time

port = 7496

FUTCONTRACT = []

# request a list of contracts
class contractApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)


    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        print(reqId, TickTypeEnum.to_str(tickType), price, attrib)
    
    def tickSize(self, reqId: TickerId, tickType: TickType, size: Decimal):
        print(reqId, TickTypeEnum.to_str(tickType), size)


def main():

    app = contractApp()
    app.connect("127.0.0.1", port, 1001)
    Thread(target=app.run).start()

    
    contract = Contract()
    contract.symbol = "BVFL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    app.reqMktData(1000, contract, "", False, False, [])
    
    contract = Contract()
    contract.symbol = "PFBX"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    app.reqMktData(2000, contract, "", False, False, [])

    time.sleep(10)

    app.disconnect()


if __name__ == "__main__":
    main()