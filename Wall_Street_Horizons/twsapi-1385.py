from ibapi.client import *
from ibapi.wrapper import *
from threading import Thread
from datetime import datetime
from time import sleep
import json, logging

port = 7497


# Configure custom logger with unique name
logger = logging.getLogger('WSHDataRequester')
logger.setLevel(logging.INFO)

# Configure IB API logger separately

# Create console handler with custom formatting
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatters - different for app vs IB API
app_formatter = logging.Formatter(
    '%(asctime)s - [APP] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create separate handlers for app and IB
app_console_handler = logging.StreamHandler()
app_console_handler.setLevel(logging.INFO)
app_console_handler.setFormatter(app_formatter)


# Add handlers to respective loggers
logger.addHandler(app_console_handler)

# Prevent propagation to root logger
logger.propagate = False

# Optional: Create file handlers for separate log files
app_file_handler = logging.FileHandler('app_detailed.log')
app_file_handler.setLevel(logging.DEBUG)
app_file_handler.setFormatter(app_formatter)
logger.addHandler(app_file_handler)

LOG_FILE = "wsh_data_logger.log"

class TestApp(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)
        self.oid = 0
    
    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} || Error:: Time of Error: {errorTime}, Error Code: {errorCode}, Error Message: {errorString}")

    
    def nextValidId(self, orderId):
        self.oid = orderId
    
    def nextId(self):
        self.oid += 1
        return self.oid

    def wshMetaData(self, reqId: TickerId, data: str):
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} || WSH Meta Data received.")

    def wshEventData(self, reqId: int, dataJson: str):
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} || Received WSH Event Data -> {dataJson}.")
        jsonDict = json.dumps(json.loads(dataJson), indent=4)

def start():
    app = TestApp()
    app.connect("127.0.0.1", port, 0)
    sleep(1)
    Thread(target=app.run).start()
    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} || Beginning run loop.")
    sleep(3)
    app.nextValidId(-1)
    sleep(1)

    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} || Request WSH Meta Data.")
    app.reqWshMetaData(app.nextId())

    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} || Request WSH Meta Data.")
    app.reqWshMetaData(app.nextId())

    eventData = WshEventData()
    eventData.filter = '{"country": "All","watchlist":["13905705"], "wshe_ed":"true"}'
    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} || Request WSH Event Data for {eventData.filter}.")
    app.reqWshEventData(app.nextId(), eventData)

if __name__ == "__main__":
    start()