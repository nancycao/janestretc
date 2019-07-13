orderID = 1

def firstbotmain(msg):
    global orderID
    #if msg["type"] == "book":
    #    print(msg)
    # selling bonds first
    order = None
    if msg["type"] == "book" and msg["symbol"] == "BOND":
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
        print(order)
        return order
