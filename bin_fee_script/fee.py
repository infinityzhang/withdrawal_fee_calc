import urllib2

exchanges = list()
exchanges.append("binance")
exchanges.append("poloniex")
exchanges.append("bittrex")
exchanges.append("kraken")
exchanges.append("cex-io") 
exchanges.append("gdax")
exchanges.append("bitgrail")

html = None

def saveFeesPage():
    print "saving fees"
    url = "https://www.binance.com/fees.html"
    page = urllib2.urlopen(url, timeout=10)
    if page.getcode() != 200:
        raise exception('failed to load page') 
    html = page.read()
    page.close()
    fh = open("fees.html", "w")
    fh.writelines(html)
    fh.close()



def saveMarket(name):
    print "saving {}".format(name)
    url = "https://coinmarketcap.com/exchanges/{}".format(name)
    page = urllib2.urlopen(url, timeout=10)
    if page.getcode() != 200:
        raise exception('failed to load page') 
    html = page.read()
    page.close()
    fh = open("{}.htm".format(name), "w")
    fh.writelines(html)
    fh.close()

import os
if not os.path.isfile("fees.html"):
    print "You must download https://www.binance.com/fees.html this page manually or save it via selenium"
    exit()
saveMarket('binance')

def savePage(url, name):
    page = urllib2.urlopen(url, timeout=10)
    if page.getcode() != 200:
        raise Exception('Failed to load page') 
    html = page.read()
    page.close()
    fh = open("saved/{}.htm".format(name), "w")
    fh.writelines(html)
    fh.close()

def saveCaps():
    url = "https://coinmarketcap.com"
    page = urllib2.urlopen(url, timeout=10)
    if page.getcode() != 200:
        raise Exception('Failed to load page') 
    html = page.read()
    page.close()
    fh = open("caps.htm", "w")
    fh.writelines(html)
    fh.close()


def getIndex():
    url = "https://coinmarketcap.com/historical"
    page = urllib2.urlopen(url, timeout=10)
    if page.getcode() != 200:
        raise Exception('Failed to load page') 
    html = page.read()
    page.close()
    fh = open("index.htm", "w")
    fh.writelines(html)
    fh.close()

def getData():
    fh = open("index.htm", "r")
    html = fh.readlines()
    fh.close()
    import re
    count = len(html)
    for i, line in enumerate(html):
        if "historical" in line:
            match = re.search(r'[0-9]+', line)
            if match:
                name = match.group()
                print "progress current {} : count {} / 3054".format(name, i, count)
                url = "https://coinmarketcap.com/historical/{}".format(name)
                savePage(url, name)

def getNames(name):
    if name == "BCC" or name == "BCH":
        return ["BCC", "BCH"]
    return [name]

def saveUpdateExchanges():
    saveCaps()
    global exchanges
    for exchange in exchanges:
        saveMarket(exchange)

def isfloat2(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


savedCaps = dict() 
def getCap(name):

    if name in savedCaps:
        return savedPriceS[name]

    fh = open("caps.htm", "r")
    html = fh.readlines()
    fh.close()

    in1 = False
    in2 = False
    in3 = False
    count = 0
    for line in html:
        if "id-{}".format(name) in line:
            in3 = True
        elif in3 and "no-wrap market-cap" in line:
            in1 = True
        elif in1 and not in2:
            in2 = True
        elif in2:
            return float(line)
    return "yea right"

# from locale import *
# setlocale(LC_NUMERIC, '')
# what = getCap("bitcoin")
# print what

savedPriceS = dict() 

def tally():
    count = dict()
    global savedPriceS
    for name in savedPriceS:
        pair = savedPriceS[name]
        if pair[1] in count:
            count[pair[1]] = count[pair[1]] + 1
        else:
            count[pair[1]] = 1

    print count


def clearPrices():
    global savedPriceS
    savedPriceS = dict()

def getPrice(name, getMax=True, market = "all"):
    name = name.upper()

    global savedPriceS

    if name in savedPriceS:
        return savedPriceS[name]

    highestPrice = None
    bestPriceSell = dict()
    global exchanges
    prices = list()
    for exchange in exchanges:
        if exchange != market and not market == "all":
            continue

#         print "Looking at {}".format(exchange)
        fh = open("{}.htm".format(exchange), "r")
        html = fh.readlines()
        fh.close()
        foundu = False 
        foundb = False 

        for altname in getNames(name):
            if foundu or foundb:
                continue

            for line in html:

                if "{}/USD".format(altname)  in line:
                    foundu = True

                if "{}/BTC".format(altname) in line:
                    foundb = True

                #print line
                if (foundu or foundb) and "price" in line:
                    tokens = line.split("\"")

                    if not isfloat2(tokens[3]):
                        continue

                    price = float(tokens[3])
                    prices.append(price)
                    break

    if len(prices) == 0:
        if not name == "USD":
            #print "\t\tCould not find prices for {}".format(name)
            return (1, "none")
        return (0, "none")

    if getMax:
        ret = (max(prices), exchanges[prices.index(max(prices))])
    else:
        ret = (min(prices), exchanges[prices.index(min(prices))])

    savedPriceS[name] = ret
    return ret

def value(coin, bal, getMax, market):
    prices = getPrice(coin, getMax, market)
    ret = prices[0] * bal
    return ret

def getPrices():
    fh = open("fees.html", "r")
    lines = fh.readlines()
    fh.close()
    for line in lines:
        if "useable f-right ng-binding" in line:
            tokens = line.split(" ")
            quantity =  float(tokens[3].split(">")[1])
            coin =  tokens[5].split("<")[0]
            cost = value(coin, quantity, True, "binance")
            cost = '${:,.2f}'.format(cost)
            print "{:5} : {:7} : Cost {}\n".format(coin, quantity, cost)

getPrices()

#saveCaps()

#saveUpdateExchanges()
# price_loc = getPrice("BCC")
