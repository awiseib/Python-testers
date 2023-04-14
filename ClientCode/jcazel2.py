import json

jBody = '[{"id":"b29e9daf-9850-425a-9521-7d45171ec6ca","message":["This order will be distributed over multiple accounts. We strongly suggest you familiarize yourself with our  allocation facilities before submitting orders."],"isSuppressed":false,"messageIds":["p6"]}]'

jRead = json.loads(jBody)[0]["id"]

print(jRead)