import sqlite3

# Common DB function definitions
def connectDB():
  '''
  Create a database on the filesystem to see how badly we understand this.
  Return the connection object.
  '''
 # myconn = ''
  try:
    myconn = sqlite3.connect('cryptcoins.db')
    myconn.execute("PRAGMA foreign_keys = 1")
    sqlite3.paramstyle = 'named'
    myconn.commit()
  except Exception as err:
    print('DOH, DB connection error')
  return myconn

def mycursor(mydb):
  '''
  Pass in a DB connection and return a viable cursor to such
  Accepts the database name as a parameter.
  '''
  mycursor = ''
  try:
    mycursor = mydb.cursor()
    mycursor.execute("""PRAGMA foreign_keys = ON""")
  except sqlite3.OperationalError as e:
    print(f'DOH! SQL Error\n {e}')
  return mycursor

def create_cointable(cur):
    '''
    Base coin table pre-population as it has cost data in it.
    Accepts cursor object as a parameter 
    '''
    try:
        cur.execute("DROP TABLE IF EXISTS coins")
        cointable = cur.execute("""CREATE TABLE coins (
                    symbol varchar(10) PRIMARY KEY, 
                    price real
                    )
              """)
    except sqlite3.OperationalError as e:
        print(f'Coin table creation failed! \n{e}')

def create_cointhisttable(cur):
    '''
    Create coin history table with an auto incrementing PK (closeid) and
    coins(symbol) as FK with close, volume, and number of trades.
    Yes, foreign keys have to come last for whatever reason. 
    '''
    try:
        cur.execute("DROP TABLE if EXISTS coinhist")
        coinhisttable = cur.execute("""CREATE TABLE coinhist (
                        closeid NUMERIC PRIMARY KEY,
                        closetime int,
                        close real,
                        volume real,
                        coin varchar(10),
                        FOREIGN KEY(coin) REFERENCES coins(symbol)          
                        )
                    """)
    except sqlite3.OperationalError as err:
        print(f'Coinhistory table creation failed! \n{err}')

def show_tables(cur):
    tables = ''
    '''
    Show talbles becuase we're in memory and can't use a table browser
    '''
    try:
      tables = cur.execute("""SELECT name FROM sqlite_master WHERE type='table' ORDER BY name DESC""")
    except sqlite3.OperationalError as err:
        print(f'Show tables failed! \n{err}')
    return tables
