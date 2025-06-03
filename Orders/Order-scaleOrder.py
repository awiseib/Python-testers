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
        order.totalQuantity = 8000
        order.lmtPrice = 17
        order.tif = 'DAY'
        
        #MAIN
        order.scaleInitLevelSize  = 1000
        order.scaleSubsLevelSize  = 200   #optional - After the initial fill of 2,000 shares switch to quantity = 100
        order.scalePriceIncrement = 0.5   #must be > 0
        order.scaleRandomPercent = False
        
        #AUTO PRICE ADJUSTMENT
        #order.scalePriceAdjustValue = .2 
        #order.scalePriceAdjustInterval = 1   
        
        #PROFIT TAKER
        order.scaleProfitOffset = 2  
        order.scaleAutoReset = False  
        #order.scaleInitPosition = 2000   #seems optional
        #order.scaleInitFillQty = 200     #seems optional
        
        #order.scaleTable = ""

        self.placeOrder(102, contract, order)

    
    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)
    
app = TradingApp()      
app.connect("127.0.0.1", port, 0)
app.run()