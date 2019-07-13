orderID = 1

globalMarketData = []

def firstbotmain(msg):
    #if msg["type"] == "book":
    #    print(msg)
    # selling bonds first
    addGlobalStateData(msg)
    if msg["type"] == "book" and msg["symbol"] == "BOND":
        return tradeBonds(msg)

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
            order = {"type": "add", "order_id": orderID, "symbol": "BOND", "dir": "BUY", "price": sellPrice, "size": sellSize}
            orderID += 1
    for buyPrice, buySize in buyList:
        if buyPrice > 1000:
            # buy under 1000
            order = {"type": "add", "order_id": orderID, "symbol": "BOND", "dir": "SELL", "price": buyPrice, "size": buySize}
            orderID += 1
    if order:
        print(order)
    return order

def addGlobalStateData(msg):
    if msg["type"] == "book":
        globalMarket[(msg["symbol"], "buy")] = msg["buy"]
        globalMarket[(msg["symbol"], "sell")] = msg["sell"]

def getFairValue(symbol):
    offers = globalMarket[(symbol, "buy")]
    bids = globalMarket[(symbol, "sell")]

    highestOffer = max(offers, key=getPrice)
    lowestBid = min(bids, key=getPrice)

    return (highestOffer + lowestBid)/2

def getPrice(item):
    return item[0]
