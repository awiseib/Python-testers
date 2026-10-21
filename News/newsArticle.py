from ibapi.client import *
from ibapi.wrapper import *

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        '''
        Please be aware this article may no longer be available. 
        If that is the case, please test the News-Historical.py request for avialable news articles.
        '''
        self.reqNewsArticle(
            reqId=orderId, 
            providerCode="DJ-N", 
            articleId="DJ-N$1f8c854d", 
            newsArticleOptions= []
        ) 

    def newsArticle(self, requestId: int, articleType: int, articleText: str):
        print("Article Type: ", articleType)
        print( articleText)

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(f"Error., Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")
        if advancedOrderRejectJson != "":
            print(f"AdvancedOrderRejectJson: {advancedOrderRejectJson}")

app = TestApp()
app.connect(host="127.0.0.1", port=7497, clientId=0)
app.run()