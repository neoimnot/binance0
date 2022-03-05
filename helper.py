from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime as dtdt
from binance.client import Client
import datetime as dt
import subprocess as sp
import requests
import smtplib 
import json
import ssl
import os

# Import environment variables
exec(open('.src/.myenv/.myenv').read())

# Set environemnt to variables
mykey=os.getenv('mykey')
mysecret=os.getenv('mysecret')
smtpPass = os.environ.get('mymailcred')

# X-MBX-APIKEY definition for the request header.
myMBXKEY = {'X-MBX-APIKEY': mykey}

# Initialize Binance Client
client = Client(mysecret, mykey, tld='us')
client.session.headers.update({'X-MBX-APIKEY': myMBXKEY.get('myMBXKEY')})

# Base and Endpoint Definitions.  BaseURL has "/" ending.
baseEP = f'https://api.binance.us/'
conntestEP = f'api/v3/ping'
svrtimeEP = f'api/v3/time'
candlestickEP = f'api/v3/klines'
tickerpriceEP = f'api/v3/ticker/price'

# Generic Function definitions next
# def get_json(url, **kwargs):
#   '''
#   Helper function to call Binance Endpoints
#   '''
#   print(url)
#   try:
#     params = {}
#     r = requests.get(url, params=params, headers=myMBXKEY)
#   except Exception as err:
#     print(f'DOH!...looks like we hit an error\n{err}')
#   return r.json()

def get_qstring(url, myparams):
  '''
  # Helper function to call Binance Endpoints
  parameters passed in as dictionary to myparams
  '''
  try:
    r = requests.get(url, headers=myMBXKEY, params=myparams)
  except json.JSONDecodeError as jerr:
    print(f'DOH! JSON error:\n{jerr.values}')
  return r.json()

def makeTS(mytime):
  '''
  Binance API returns their timestamps in milliseconds.
  Remove them and convert remainder to datetime.datetime object.
  '''
  mytime = int(mytime/1000)
  return dt.fromtimestamp(mytime)

def create200TStamps():
  '''
  Create two Binance friendly timestamps.  One from now and one from 201 days ago
  Retun as a tuple.
  '''
  mynow = dtdt.now()
  mystartTime = dt.timedelta(201)
  return (round(mynow.timestamp() * 1000), round((mynow - mystartTime).timestamp() * 1000))

def genBinanceTS():
  '''
  Binance API timestamps need to be in milliseconds.
  Return exactly that. 
  '''
  return sp.call(['date', '+%s000'])

def chckcon():
  try:
    return client.get_server_time()
  except Exception as err:
    print('Binance Client error')

def mycoins():
  try:
    return client.get_all_tickers()
  except Exception as err:
    print('Binance Client error') 

def myaccount():
    try:
        myinfo = client.get_account()
        return myinfo
    except Exception as e:
      print(e)
      print()
      print(client.response.headers)

def tickerInfo(sym):
  pass
