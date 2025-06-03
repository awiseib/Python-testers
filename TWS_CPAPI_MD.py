# Library Imports

# CPAPI
from ibapi.common import TickAttrib, TickerId
import requests
import time
import urllib3
import ssl
import json
import websocket
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TWS API
from ibapi.client import *
from ibapi.wrapper import *
import csv
from datetime import datetime
import threading
from ibapi.ticktype import TickType, TickTypeEnum

port = 7496

conid = 620730945
md_dict = {"conid": conid}
# {symbol, conid, twsLast, cpLast}

# TWS Start
class TestApp(EClient, EWrapper):
  def __init__(self):
    EClient.__init__(self,self)

  def nextValidId(self, orderId: int):
    contract = Contract()
    contract.conId = conid
    contract.exchange = "CME"

    self.reqMktData(orderId, contract,"", 0,0,[])
  
  def tickPrice(self, reqId: int, tickType: int, price: float, attrib: TickAttrib):
    if TickTypeEnum.toStr(tickType) == "LAST":
        md_dict["twsLast"] = price


# CPAPI Start
def confirmStatus():
    base_url = "https://localhost:5001/v1/api/tickle"
    
    auth_req = requests.post(url=base_url,verify=False)
    print(auth_req.content)
    return auth_req.json()['session']

def on_message(ws, message):
    jmsg = json.loads(message.decode('utf-8'))

    if "smd" in jmsg["topic"]:
       if "55" in jmsg.keys():
          md_dict["symbol"] = jmsg["55"]
       if "31" in jmsg.keys():
          md_dict["cpLast"] = jmsg["31"]
    threading.Thread(target=comparison).start()

def on_error(ws, error):
    print(error)

def on_close(ws, msg1, msg2):
    print("## CLOSED! ##")
    print(msg1)
    print(msg2)

def on_open(ws):
    print("Opened Connection")
    time.sleep(1)
    ws.send('smd+%s+{"fields":["55","31"]}' % conid)

def comparison():
#    while True:
    try:
        print(f"symbol: {md_dict['symbol']} cpLast: {md_dict['cpLast']} || twsLast: {md_dict['twsLast']}")
    except KeyError:
        pass
    # time.sleep(0.5)

if __name__ == "__main__":
    # TWS Start
    app = TestApp()
    app.connect("127.0.0.1", 7496, 0)
    threading.Thread(target=app.run).start()

    # threading.Thread(target=comparison).start()

    # CPAPI Start
    session_token = confirmStatus()
    print(session_token)
    ws = websocket.WebSocketApp(
        url="wss://localhost:5001/v1/api/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        cookie=f"api={session_token}"
    )
    ws.run_forever(sslopt={"cert_reqs":ssl.CERT_NONE})