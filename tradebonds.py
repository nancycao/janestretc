def tradeBonds(msg):
    global orderID
    buyOrder, sellOrder = None
    sellList = msg["sell"]
    buyList = msg["buy"]
    minBuy = float("inf")
    maxSell = float("-inf")
    for sellPrice, sellSize in sellList:
        #print(sellPrice)
        #print(sellList)
        if sellPrice < 1000:
            # buy under 1000
            if sellPrice < minBuy:
                minBuy = sellPrice
                buyOrder = {"type": "add", "order_id": orderID, "symbol": "BOND", "dir": "BUY", "price": sellPrice-1, "size": sellSize}
                orderID += 1
    for buyPrice, buySize in buyList:
        if buyPrice > 1000:
            # buy under 1000
            if buyPrice > maxSell:
                maxSell = maxPrice
                sellOrder = {"type": "add", "order_id": orderID, "symbol": "BOND", "dir": "SELL", "price": buyPrice+1, "size": buySize}
                orderID += 1
    if buyOrder != None:
        orderList.append(buyOrder)
    if sellOrder != None:
        orderList.append(sellOrder)
    return orderList
