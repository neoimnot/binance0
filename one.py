from helper import * 
from deebee import *

# Initialize Connection and cursor variables before assignment
conn = None
cursor = None

# Connect to db, initiaize cursor, and create table
conn = connectDB()
cursor = mycursor(conn)
create_cointable(cursor)
create_cointhisttable(cursor)

#Show table creation
mytables = show_tables(cursor)
#print(mytables.fetchall())

# Fetch coin names and closing
thecoins = mycoins()
# print(f'This is the variable thecoins\n{thecoins}') 

def popultate_coinhisttable(mylist, mycoin):
  '''
  Accept a coin-name and list of lists of kline data for 201 days. Retun data
  appears as a tuple.  Insert into the coinhist table. 
  (0, [1629158400000, '45904.0800', '47165.9700', '44357.2600', '44679.6800', '1862.22915800', 
  1629244799999, '85232893.5862', 90489, '920.41757500', '42134160.4555', '0'])
  '''
  try:
    for sublist in enumerate(mylist):
     cursor.execute("INSERT INTO coinhist VALUES (:closeid, :closetime, :close, :volume, :coin)", 
       {'closeid': sublist[0], 'closetime': convert_timestamp(sublist[1][6]), 'close': f'{float(sublist[1][4]):.2f}',
         'volume': f'{float(sublist[1][5]):.2f}', 'coin': mycoin}) 
  except  sqlite3.IntegrityError as sql3IE:
       print(f'DOH! Inteigrity Error(populate_Coinhistorytable) as:\n{sql3IE}')
  except sqlite3.OperationalError as sql3err: 
       print(f'DOH! this is the except clause from populteCoinHistTable function \n {sql3err}')
  finally:
    conn.commit()

def fetch_coinhistory(mycoin):
  '''
  Pass in a symbol and retriev 201 days of kline data
   [1628899200000, '47836.2900', '48177.5300', '46039.0800', '47100.2900', 
   '1395.72508200', 1628985599999, '65535889.6275', 49628, '688.88120100', 
   '32352286.5264', '0']
   '''
# Initialze fetch
  fetch = ''
# Set 201 days timeframe
  mytimeRange =  create_200timestamp()
# Retrieve total number of coins
# Fetch data by coin name.
  try:
    fetch = get_qstring('https://api.binance.us/api/v3/klines',
        {'symbol': mycoin, 'interval':'1d', 'startTime':mytimeRange[1], 
        'endTime':mytimeRange[0]})
  except Exception as err:
    print(f'DOH!  Exception caught in fetch_coinhistory')
  return fetch 

def populate_cointable(coin):
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

def count_coins():
    '''
    Quick count of total number symbol names for upper limit of range() 
    '''
    mycount = 0 
    try:
      mycountq = cursor.execute("""SELECT COUNT(symbol) from coins""")
    except Exception as err:
      print(f'This is the except from the countcoins function\n{err}')
    return mycountq.fetchall()[0][0]

print(thecoins[:3])


[populate_cointable(x) for x in thecoins]
sp.call('/bin/sleep 5', shell='true')

myfetch = fetch_coinhistory('BTCUSD')
mypop = popultate_coinhisttable(myfetch, 'BTCUSD')


cursor.close()
