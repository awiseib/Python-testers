import websocket
import time
import ssl

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    time.sleep(3)
    myConids = ["265598", "8314"]
    for i in myConids:
        ws.send('smd+'+i+'+{"fields":["31","84","86"]}')


if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://localhost:5000/v1/api/ws",
                                on_open = on_open,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})