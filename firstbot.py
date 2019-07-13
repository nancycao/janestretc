import tradebonds

orderID = 1

globalMarketData = {}
globalMarketData[("VALBZ", "buy")] = None

def firstbotmain(msg):
    #if msg["type"] == "book":
    #    print(msg)
    # selling bonds first
    if msg["type"] == "book":
        if msg["symbol"] == "BOND":
            return tradebonds.tradeBonds(msg)
