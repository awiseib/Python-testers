from ibapi.client import *
from ibapi.wrapper import *
import csv
from threading import Thread
from time import sleep
from datetime import datetime

port = 7496

headers = ["Symbol", "SecType", "Exchange", "Description"]
filePath = "./NewsSources.csv"
contract_csv_file = open(filePath, 'w', newline='')
contract_writer = csv.DictWriter(f=contract_csv_file, fieldnames=headers)
contract_writer.writeheader()

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        con_dict = {}
        con_dict["Symbol"] = contractDetails.contract.symbol
        con_dict["SecType"] = contractDetails.contract.secType
        con_dict["Exchange"] = self.con_tracker[reqId]
        con_dict["Description"] = contractDetails.contract.tradingClass
        
        contract_writer.writerow(con_dict)
    
    def contractDetailsEnd(self, reqId):
        print(f"Finished {self.con_tracker[reqId]} at {datetime.now()}")
        
    def error(self, reqId: TickerId, errorTime: int, errorCode: int, errorString: str, advancedOrderRejectJson=""):
        print(reqId, errorCode, errorString, advancedOrderRejectJson)
        
def time_to_die():
    sleep(15)
    app.disconnect()
    contract_csv_file.close()

app = TestApp()
app.connect("127.0.0.1", port, 0)
sleep(2)
Thread(target=app.run).start()

app.con_tracker = {}

oid = 1
for news_source in ["BRFG", "BRFUPDN", "DJ", "DJNL", "FLY", "BZ", "DJTOP"]: # These are the values you can pass as an exchange
    contract = Contract()
    contract.secType = "NEWS"
    contract.exchange = news_source
    
    app.con_tracker[oid] = news_source
    print(f"started  {news_source} at {datetime.now()}")
    app.reqContractDetails(reqId=oid, contract=contract)
    oid+=1
Thread(target=time_to_die).start()
