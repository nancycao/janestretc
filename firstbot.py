import tradebonds

orderID = 1

globalMarketData = {}

def firstbotmain(msg):
    #if msg["type"] == "book":
    #    print(msg)
    # selling bonds first
    if msg["type"] == "book":
        if msg["symbol"] == "BOND":
             return tradebonds.tradeBonds(msg)
        #if msg["symbol"] == "VALBZ" or msg["symbol"] == "VALE":
        #    return tradeADR(msg)

def tradeADR(msg):
    fairValue = getFairValue("VALBZ")
    sellList = msg["sell"]
    buyList = msg["buy"]
    for sellPrice, sellSize in sellList:
        #print(sellPrice)
        #print(sellList)
        if sellPrice < fairValue:
            # buy under 1000
            order = {"type": "add", "order_id": orderID, "symbol": msg["symbol"], "dir": "BUY", "price": sellPrice-1, "size": sellSize}
            orderID += 1
    for buyPrice, buySize in buyList:
        if buyPrice > fairValue:
            # buy under 1000
            order = {"type": "add", "order_id": orderID, "symbol": msg["symbol"], "dir": "SELL", "price": buyPrice+1, "size": buySize}
            orderID += 1
    if order:
        print(order)
    return order

def addGlobalStateData(msg):
    if msg["type"] == "book":
        globalMarketData[(msg["symbol"], "buy")] = msg["buy"]
        globalMarketData[(msg["symbol"], "sell")] = msg["sell"]

def getFairValue(symbol):
    offers = globalMarketData[(symbol, "buy")]
    bids = globalMarketData[(symbol, "sell")]

    highestOffer = max(offers, key=getPrice)
    lowestBid = min(bids, key=getPrice)

    return (highestOffer + lowestBid)/2

def getPrice(item):
    return item[0]
