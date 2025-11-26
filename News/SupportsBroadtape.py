from ibapi.client import *
from ibapi.wrapper import *
from threading import Thread
from time import sleep
import csv

port = 7496

headers = ["Symbol", "SecType", "Exchange", "Description", "Supports Broadtape"]
filePath = r"C:\Users\awise\Code\Python testers\BroadtapeNewsSupport.csv"
contract_csv_file = open(filePath, 'w', newline='')
contract_writer = csv.DictWriter(f=contract_csv_file, fieldnames=headers)
contract_writer.writeheader()

success_check = {}

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def tickNews(self, tickerId: int, timeStamp: int, providerCode: str, articleId: str, headline: str, extraData: str):
        if success_check[tickerId]["Supports Broadtape"] == None:
            success_check[tickerId]["Supports Broadtape"] = True
            self.cancelMktData(tickerId)
            contract_writer.writerow(success_check[tickerId])

    def tickString(self, reqId: TickerId, tickType: TickType, value: str):
        if success_check[reqId]["Supports Broadtape"] == None:
            success_check[reqId]["Supports Broadtape"] = True
            self.cancelMktData(reqId)
            contract_writer.writerow(success_check[reqId])

    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        if reqId > 0 and reqId in success_check.keys() and success_check[reqId]["Supports Broadtape"] == None and errorCode != 300:
            success_check[reqId]["Supports Broadtape"] = False
            contract_writer.writerow(success_check[reqId])
            self.cancelMktData(reqId)
        elif errorCode != 300:
            print(f"Error for {reqId}, Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")

def time_to_die():
    sleep(300)
    app.disconnect()
    contract_csv_file.close()
    newsContractFile.close()

app = TestApp()
app.connect("127.0.0.1", port, 0)
sleep(2)
Thread(target=app.run).start()
try:
    newsContractFile = open(r"C:\Users\awise\Code\Python testers\NewsSources.csv", "r")
    newsContractHeaders = ["Symbol","SecType","Exchange", "Description"]
    newsFileReader = csv.DictReader(f=newsContractFile, fieldnames=newsContractHeaders)
except FileNotFoundError as e:
    print(e)
    app.disconnect()
    exit()

row_num = 0
for news_contract in newsFileReader:
    if news_contract["Symbol"] == "Symbol":
        continue
    success_check[row_num] = {
        "Symbol": news_contract["Symbol"],
        "SecType": news_contract["SecType"],
        "Exchange": news_contract["Exchange"],
        "Description": news_contract["Description"],
        "Supports Broadtape": None
    }

    contract = Contract()
    contract.symbol = news_contract["Symbol"]
    contract.secType = "NEWS"
    contract.exchange = news_contract["Exchange"]

    app.reqMktData(
        reqId=row_num,
        contract=contract,
        genericTickList="mdoff,292",
        snapshot=False,
        regulatorySnapshot=False,
        mktDataOptions=[],
    )
    row_num += 1
    sleep(0.05)
time_to_die()