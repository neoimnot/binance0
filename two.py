from helper import *

# Intitalize db
#myconn = sqlite3.connect('coindata.db')
# Function defintions
def account():
    '''
    # For signed requests we create an Account instance and give it the api key and secret
    '''    
    print("\nAccount data examples\n")
    account = binance.Account(mykey, mysecret)
    account.set_receive_window(5000)

def market_data():
    '''
    ping binance to see if it's online and verify we can hit it
    '''
    print("\nMarket data examples\n")
    print("Connection ok? ", binance.ping())

    #Get the current server time in milliseconds
    print("Server time: ", binance.server_time())

def makedate(mytime):
  '''
  Binance API appears to pad their timestamps with three zeros at the end
  Remove them and convert remainder to datetime.datetime object.
  '''
  mytime = int(mytime/1000)
  return dt.fromtimestamp(mytime)

#myAccount = account()
#print(myAccount)

serverstat = get_json(f'{baseEP}{svrtimeEP}')
print(parseserverstat(serverstat.get('serverTime')))

symbols = get_json(f'{baseEP}{tickerpriceEP}')
for item in symbols:
    print(item)

#symbolinfo = clitickerklines = client.get_klines(symbol='BNBBTC', interval='1D')ent.get_symbol_info('BNBBTC')
#tickerklines = client.get_klines(symbol='BNBBTC', interval=client.KLINE_INTERVAL_1DAY)
#tickerinfo = client.


#print(client.response.headers)

# tickerklines is list of lists
#print(makedate(tickerklines[0][0]))

#for item in tickerklines:
#    print(makedate(item[0]),item[1:])
