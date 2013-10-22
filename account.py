#!/bin/python
import os
import oauth2 as oauth
import json

#Constants
# key/secrets for authentication
_CONSUMER_KEY_          = 'm1sIVuD5kiOj9ZHXe7K2VlZjBDham6dS2yBqVNBs'
_CONSUMER_SECRET_       = 'kE9exMYtPJVCpZYSCeyKJq4gDEJc8eN5tf0WXbEQ'
_ACCESS_TOKEN_          = 'Wvnx3G9idazJvk2sADJcZDOKs3YRrIHNQV1sAIiW'
_ACCESS_TOKEN_SECRET_   = 'je9oTDZXGG07geEBfIe6zS58iJ9PiLMGhLzAahRZ'
_BASE_URL_              = "https://api.tradeking.com/v1"
_ACCOUNT_NUMBER_        = 60532703

token    = oauth.Token(key=_ACCESS_TOKEN_, secret=_ACCESS_TOKEN_SECRET_)
consumer = oauth.Consumer(key=_CONSUMER_KEY_, secret=_CONSUMER_SECRET_)
request_holdings_url = "%s/accounts/%s/holdings.json" % (_BASE_URL_, _ACCOUNT_NUMBER_)
request_values_url = "%s/market/ext/quotes.xml?" % _BASE_URL_
#creating the client
client = oauth.Client(consumer, token=token)
client.ca_certs = os.path.join(os.path.dirname(__file__), 'cacert.pem')

#making the request via the client

stocksym = {}


def urlquery():
# get all of my tradeking info
    resp, content = client.request(request_holdings_url, "GET")
    content =  json.loads(content)
    return content


def getstocksym(json):
    # returns the holdings under my TK acct
    allholdings = json[u"response"][u"accountholdings"][u"holding"]
    for stock in allholdings:
        sym = stock[u"instrument"][u"sym"]
        stocksym.update({sym: 0})
    return stocksym


def stockvalue(stocks):
    # returns a dictionary with stock: price: change:
    stockvalues = {}
    for stock in stocks:
        resp, content = client.request("https://api.tradeking.com/v1/market/ext/quotes.json?symbols=%s" % stock, "GET")
        content = json.loads(content)
        change = content[u"response"][u"quotes"][u"quote"][u"chg_sign"]
        price = content[u"response"][u"quotes"][u"quote"][u"ask"]
        stockvalues.update({stock: {'price':price, 'change':change}})
    return stockvalues

def parsevalues(stockvalues):
    #parses library, returns whether or not a stock in the dictionary is changing, and what price it is.
    values = []
    for stock in stockvalues:
        price = stockvalues[stock][u"price"]
        if stockvalues[stock][u"change"] == 'u':
            return "%s is going up! and the price is: %s" % (stock, price)
        elif stockvalues[stock][u"change"] == 'd':
           return "%s is going down! and the price is %s" % (stock, price)


if __name__ == "__main__":
   parsevalues(stockvalue(getstocksym(urlquery())))
