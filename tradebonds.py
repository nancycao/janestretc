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
