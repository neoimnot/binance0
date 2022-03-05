from helper import * 
from deebee import *

# Initialize Connection and cursor variables before assignment
conn = None
cursor = None

# Connect to db, initiaize cursor, and create table
conn = connectDB()
cursor = mycursor(conn)
createCoinTable(cursor)
createCointHistTable(cursor)

#Show table creation
mytables = showTables(cursor)
print(mytables.fetchall())

# Fetch coin names and closing
thecoins = mycoins()
# print(f'This is the variable thecoins\n{thecoins}') 

def popultateCoinHistTable(mycoin):
   '''
   Fetch a tuple of binance ready timestamps 201 days apart.  Then
   call the API for the symbol passed in for that range.  Update
   the coinhist table with those values.
   Endpoint 'klines' returns a list, e.g.,
   [1628899200000, '47836.2900', '48177.5300', '46039.0800', '47100.2900', 
   '1395.72508200', 1628985599999, '65535889.6275', 49628, '688.88120100', 
   '32352286.5264', '0']
   '''
#  Initialze fetch and mycount
   fetch = ''
   coincount = 0 
#   Set 201 days timeframe
   mytimeRange =  create200TStamps()
#  How many coins?
   coincount = countcoins()
#   Fetch data by coin name.
   try:
     fetch = get_qstring('https://api.binance.us/api/v3/klines',
         {'symbol': mycoin, 'interval':'1d', 'startTime':mytimeRange[1], 
         'endTime':mytimeRange[0]})
   except Exception as err:
     print(f'DOH! This is the except from populateCoinHistTable\n{err}')
   finally:
     try:
        if fetch:
          for sublist in fetch:
            for num in range(1, coincount):
              cursor.execute("INSERT INTO coinhist VALUES (:closeid, :close, :volume, :coin)", 
                {'closeid': num, 'close': f'{float(sublist[4]):.2f}',
                 'volume': f'{float(sublist[5]):.2f}','coin': str(mycoin)}
          )
        else:
          print(f'This is the else from the cursor.execute')
     except  sqlite3.IntegrityError as sql3IE:
       print(f'DOH! Inteigrity Error as\n{sql3IE}')
     except sqlite3.OperationalError as sql3err: 
       print(f'DOH! this is the except clause from populteCoinHistTable function \n {sql3err}')
#tPrice = get_json(f'{baseEP}{tickerpriceEP}')
#tickerklines = get_qs(f'{baseEP}{candlestickEP}', params={'symbol':'LTCBTC', 'interval':client.KLINE_INTERVAL_1DAY, 'startTime':1642550399999, 'endTime':1643587199999})
#tickerklines = get_qstring(f'{baseEP}{candlestickEP}', {'symbol':'LTCBTC', 'interval':'1d','startTime':1642550399999, 'endTime':1643587199999})

# Print Request headers
#print(client.response.headers)

#tickerklines is list of lists
#print(makedate(tickerklines[0][0]))
#print(thecoins[0])

# for subdict in thecoins:
#   print(subdict.get('symbol'), '{:.2f}'.format(float(subdict.get('price'))))

def populateCoinTable(coin):
   try:
    cursor.execute("INSERT INTO coins VALUES (:symbol, :price)", 
      {'symbol': coin.get('symbol'), 'price': coin.get('price')})
   except  sqlite3.IntegrityError as sql3IE:
       print(f'DOH! this is the except clause (InteigrityError) as\n{sql3IE}')
   except sqlite3.OperationalError as sql3err: 
       print(f'DOH! this is the except clause (OperationalError) populteCoinTable function \n {sql3err}')       
   except Exception as err:
     print(f'DOH! This is the except (General) from populateCoinTable\n{err}')
   finally:
      conn.commit()

[populateCoinTable(x) for x in thecoins]
sp.call('/bin/sleep 5', shell='true')
[popultateCoinHistTable(x) for x in thecoins]
# myq = cursor.execute('select * from coins')
# print(myq.fetchmany(5))

# for subdict in thecoins:
#   popultateCoinHistTable(str(subdict.get('symbol')))
#   print(str(subdict.get('symbol')))

# wtf = popultateCoinHistTable('SUSHIUSDT') 
# print(f'This is wtf: {wtf}')     

#Show table contents
# myquery = cursor.execute('SELECT * from coins')
# print(f'This is coming from the in-memory database\n{[coin for coin in myquery.fetchmany(10)]})')

#Show table contents
# coinHistQuery = cursor.execute('SELECT * from coins')
# print(f'This is coming from the in-memory database\n{[coin for coin in coinHistQuery.fetchmany(10)]})')


cursor.close()
