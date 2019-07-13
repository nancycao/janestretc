orderID = 1

def firstbotmain(msg):
    #if msg["type"] == "book":
    #    print(msg)
    # selling bonds first
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
