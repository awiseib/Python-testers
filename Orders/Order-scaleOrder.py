from ibapi.client import *
from ibapi.wrapper import *

port = 7496

class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)
        
    def nextValidId(self, orderId):
        contract = Contract()
        contract.symbol = "AAPL"
        contract.exchange = "SMART"
        contract.secType = "STK"
        contract.currency = "USD"
        
        order = Order()
        order.action = "BUY"
        order.orderType = "LMT"        
        order.totalQuantity = 1111          # TotalQuantity becomes Maximum Position for Scale Orders.
        order.lmtPrice = 17
        order.tif = 'DAY'
        
        #MAIN
        order.scaleInitLevelSize  = 222     # Initial Component Size
        order.scaleSubsLevelSize  = 33      # Subsequent Comp. Size
        order.scalePriceIncrement = 10      # Price Increment
        order.scaleRandomPercent = False    # Randomize size by +/- 55%
        
        #AUTO PRICE ADJUSTMENT
        order.scalePriceAdjustValue = 4     # Increase starting price by _
        order.scalePriceAdjustInterval = 5  # Increase starting price every _
        
        #PROFIT TAKER
        order.scaleProfitOffset = 6         # Profit Orders' Profit Offset
        order.scaleAutoReset = False        # Profit Orders' Restore size after taking profit
        order.scaleInitPosition = 7         # Profit Orders' Initial Position
        order.scaleInitFillQty = 8          # Profit Orders' Filled Initial Component Size
        
        self.placeOrder(102, contract, order)

    
    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)
    
app = TradingApp()      
app.connect("127.0.0.1", port, 0)
app.run()