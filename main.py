import requests, json

rawdata = requests.get('https://api.coingate.com/v2/rates').json()
tradeables = ["LTC", "ETH", "XRP", "DOGE", "USDT"]
valuablepairs = {}

for firsthop in tradeables:
    for secondhop in tradeables:
        if secondhop == firsthop: continue
        priceindex2 = 1.0
        priceindex2 = priceindex2 * float(rawdata["merchant"]["BTC"][firsthop])
        priceindex2 = priceindex2 * float(rawdata["merchant"][firsthop][secondhop])
        priceindex2 = priceindex2 * float(rawdata["merchant"][secondhop]["BTC"])
        valuablepairs[str("BTC>" + firsthop + ">" + secondhop + ">BTC")] = priceindex2
        for thirdhop in tradeables:
            if thirdhop == firsthop: continue
            if thirdhop == secondhop: continue
            priceindex3 = 1.0
            priceindex3 = priceindex3 * float(rawdata["merchant"]["BTC"][firsthop])
            priceindex3 = priceindex3 * float(rawdata["merchant"][firsthop][secondhop])
            priceindex3 = priceindex3 * float(rawdata["merchant"][secondhop][thirdhop])
            priceindex3 = priceindex3 * float(rawdata["merchant"][thirdhop]["BTC"])
            valuablepairs[str("BTC>" + firsthop + ">" + secondhop + ">" + thirdhop + ">BTC")] = priceindex3
            for fourthhop in tradeables:
                if fourthhop == firsthop: continue
                if fourthhop == secondhop: continue
                if fourthhop == thirdhop: continue
                priceindex4 = 1.0
                priceindex4 = priceindex4 * float(rawdata["merchant"]["BTC"][firsthop])
                priceindex4 = priceindex4 * float(rawdata["merchant"][firsthop][secondhop])
                priceindex4 = priceindex4 * float(rawdata["merchant"][secondhop][thirdhop])
                priceindex4 = priceindex4 * float(rawdata["merchant"][thirdhop][fourthhop])
                priceindex4 = priceindex4 * float(rawdata["merchant"][fourthhop]["BTC"])
                valuablepairs[str("BTC>" + firsthop + ">" + secondhop + ">" + thirdhop + ">" + fourthhop + ">BTC")] = priceindex4

for key, value in sorted(valuablepairs.items(), key=lambda x: x[1]): 
    print("{} : {}".format(key, value))
