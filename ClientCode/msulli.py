from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue
from datetime import datetime
from threading import Thread
import time

port = 7496

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.orderId = 0

    def nextValidId(self, orderId: int):
        self.orderId = orderId

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(orderId, contract, order, orderState)

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(reqId, contract, execution)
    
    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)


# ! [darkice_params]
@staticmethod
def FillDarkIceParams(baseOrder, displaySize, startTime, endTime, allowPastEndTime):
    baseOrder.algoStrategy = "DarkIce"
    baseOrder.algoParams = []

    # displaySize is required
    # Will use the absolute value of 0 or greater
    baseOrder.algoParams.append(TagValue("displaySize", displaySize))

    # Not required str
    # Designates when the algo will start and end
    # Automatically uses today's date
    # Only accepts time in UTC.
    baseOrder.algoParams.append(TagValue("startTime", startTime))
    baseOrder.algoParams.append(TagValue("endTime", endTime))

    # Not required
    # Can be left out
    # Allow order to take place after specified: Y/N
    baseOrder.algoParams.append(TagValue("allowPastEndTime",int(allowPastEndTime)))
# ! [darkice_params]


# ! [ad_params]
@staticmethod
def FillAccumulateDistributeParams(baseOrder: Order, componentSize, timeBetweenOrders, randomizeTime20, randomizeSize55,
                                    giveUp, catchUp, waitForFill, startTime, endTime):
    baseOrder.algoStrategy = "AD"
    baseOrder.algoParams = []

    # Required integer
    # Decides incrementation size
    # Must be smaller than totalQuantity of the order
    baseOrder.algoParams.append(TagValue("componentSize", componentSize))
    
    # Required integer
    # Decides interval of order scaling
    # Can be as little as 0
    baseOrder.algoParams.append(TagValue("timeBetweenOrders", timeBetweenOrders))

    # Not Required
    # Can be used to help "hide the pattern" of an individual trader
    baseOrder.algoParams.append(TagValue("randomizeTime20", int(randomizeTime20)))

    # Not Required boolean
    # Can be used to help "hide the pattern" of an individual trader
    baseOrder.algoParams.append(TagValue("randomizeSize55", int(randomizeSize55)))
    
    # Not Required integer
    # If anything fails to fill per algo specs, kill the order
    baseOrder.algoParams.append(TagValue("giveUp", giveUp))

    # Not Required boolean
    # If the algo lags behind, for one reason or another, ask to fire off new orders to catch up
    baseOrder.algoParams.append(TagValue("catchUp", int(catchUp)))

    # Not Required integer
    # Decides if the order should wait for the last increment to be filled
    baseOrder.algoParams.append(TagValue("waitForFill", int(waitForFill)))

    # Not required str
    # Designates when the algo will start and end
    # Automatically uses today's date
    # Only accepts time in UTC.
    baseOrder.algoParams.append(TagValue("activeTimeStart", startTime))
    baseOrder.algoParams.append(TagValue("activeTimeEnd", endTime))
# ! [ad_params]


app = TestApp()
app.connect("127.0.0.1", port, 1001)
Thread(target=app.run).start()
time.sleep(3)

contract = Contract() # AAPL STK Contract
contract.conId=265598 
contract.exchange="SMART"

order = Order() # Simple Order object
order.action = "BUY"
order.orderType = "LMT"
order.lmtPrice = 165.00
order.totalQuantity = 15

# Test Dark Ice
# dIceOrder = order
# FillDarkIceParams(dIceOrder, 1, "", "", False)
# app.placeOrder(app.orderId, contract, dIceOrder)

# # Test Acc/Dist
accDistOrder = order
FillAccumulateDistributeParams(accDistOrder, 5, 0, False, False, 0, False, True, "", "")
app.placeOrder(app.orderId, contract, accDistOrder)