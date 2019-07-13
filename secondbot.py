import tradebonds

orderID = 1

globalMarketData = {}
seenVALBZ = False

def secondbotmain(msg):
    #if msg["type"] == "book":
    #    print(msg)
    # selling bonds first
    global seenVALBZ
    addGlobalStateData(msg)
    if msg["type"] == "book":
        if msg["symbol"] == "BOND":
             return tradebonds.tradeBonds(msg)
        if msg["symbol"] == "VALBZ":
            seenVALBZ = True
            return tradeADR(msg)
        if msg["symbol"] == "VALE" and seenVALBZ:
            #print("VALE")
            #print(globalMarketData[("VALBZ", "buy")])
            return tradeADR(msg)
        if msg["symbol"] == "MS" or msg["symbol"] == "GS" or msg["symbol"] == "WFC":
            return tradeRegStocks(msg)
        if msg["symbol"] == "XLF":
            return tradeXLF(msg)

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
    return order

def tradeADR(msg):
    global orderID
    fairValue = getFairValue("VALBZ")
    orderList = []
    sellList = msg["sell"]
    buyList = msg["buy"]
    if fairValue:
        for sellPrice, sellSize in sellList:
            #print(sellPrice)
            #print(sellList)
            if sellPrice < fairValue:
                # buy under 1000
                order = {"type": "add", "order_id": orderID, "symbol": msg["symbol"], "dir": "BUY", "price": sellPrice-1, "size": sellSize}
                orderID += 1
                orderList.append(order)
        for buyPrice, buySize in buyList:
            if buyPrice > fairValue:
                # buy under 1000
                order = {"type": "add", "order_id": orderID, "symbol": msg["symbol"], "dir": "SELL", "price": buyPrice+1, "size": buySize}
                orderID += 1
                orderList.append(order)
    return orderList

def tradeRegStocks(msg):
    global orderID
    symbol = msg["symbol"]
    fairValue = getFairValue(msg["symbol"])
    if fairValue:
        fairValue *= 0.9999
    orderList = []
    sellList = msg["sell"]
    buyList = msg["buy"]
    if fairValue:
        for sellPrice, sellSize in sellList:
            #print(sellPrice)
            #print(sellList)
            if sellPrice < fairValue:
                # buy under 1000
                order = {"type": "add", "order_id": orderID, "symbol": symbol, "dir": "BUY", "price": sellPrice, "size": sellSize}
                orderID += 1
                orderList.append(order)
        for buyPrice, buySize in buyList:
            if buyPrice > fairValue:
                # buy under 1000
                order = {"type": "add", "order_id": orderID, "symbol": symbol, "dir": "SELL", "price": buyPrice, "size": buySize}
                orderID += 1
                orderList.append(order)
    return orderList

def tradeXLF(msg):
    global orderID
    symbol = msg["symbol"]
    fairValue = getFairValue("XLF")
    if fairValue:
        fairValue *= 0.999
    orderList = []
    sellList = msg["sell"]
    buyList = msg["buy"]
    if fairValue:
        for sellPrice, sellSize in sellList:
            #print(sellPrice)
            #print(sellList)
            if sellPrice < fairValue:
                # buy under 1000
                print("XLF")
                order = {"type": "add", "order_id": orderID, "symbol": "XLF", "dir": "BUY", "price": sellPrice, "size": sellSize}
                orderID += 1
                orderList.append(order)
        for buyPrice, buySize in buyList:
            if buyPrice > fairValue:
                # buy under 1000
                print("XLF")
                order = {"type": "add", "order_id": orderID, "symbol": "XLF", "dir": "SELL", "price": buyPrice, "size": buySize}
                orderID += 1
                orderList.append(order)
    return orderList

def addGlobalStateData(msg):
    if msg["type"] == "book":
        globalMarketData[(msg["symbol"], "buy")] = msg["buy"]
        globalMarketData[(msg["symbol"], "sell")] = msg["sell"]

def getFairValue(symbol):
    offers = globalMarketData[(symbol, "buy")]
    bids = globalMarketData[(symbol, "sell")]

    if offers and bids:

        highestOffer = max(offers, key=getPrice)
        lowestBid = min(bids, key=getPrice)

        return (highestOffer[0] + lowestBid[0])/2

    return None

def getPrice(item):
    return item[0]
