globalMarket = []

def globalStateData(msg):
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

