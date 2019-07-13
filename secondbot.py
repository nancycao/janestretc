import tradebonds

orderID = 1

globalMarketData = {}
globalMarketData[("VALBZ", "buy")] = None

def firstbotmain(msg):
    #if msg["type"] == "book":
    #    print(msg)
    # selling bonds first
    addGlobalStateData(msg)
    print(globalMarketData)
    if msg["type"] == "book":
    #     if msg["symbol"] == "BOND":
    #         return tradeBonds(msg)
        if msg["symbol"] == "VALBZ":
            return tradeADR(msg)
        elif msg["symbol"] == "VALE" and globalMarketData[("VALBZ", "buy")] != None:
            return tradeADR(msg)

def tradeBonds(msg):
    global orderID
    order = None
    sellList = msg["sell"]
    buyList = msg["buy"]
    for sellPrice, sellSize in sellList:
        #print(sellPrice)
        #print(sellList)
        if sellPrice < 1000:
            # buy under 1000
            order = {"type": "add", "order_id": orderID, "symbol": "BOND", "dir": "BUY", "price": sellPrice-1, "size": sellSize}
            orderID += 1
    for buyPrice, buySize in buyList:
        if buyPrice > 1000:
            # buy under 1000
            order = {"type": "add", "order_id": orderID, "symbol": "BOND", "dir": "SELL", "price": buyPrice+1, "size": buySize}
            orderID += 1
    if order:
        print(order)
    return order

def tradeADR(msg):
    fairValue = getFairValue("VALBZ")
    order = None
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

    return (highestOffer[0] + lowestBid[0])/2

def getPrice(item):
    return item[0]
