--- ENVIRONMENT HELP ---
API keys required:
os.environ['mykey'] = [value]
os.environ['mysecret'] = [value]
os.environ['mymailcred'] = [value]
os.environ['mysender'] = [value]
os.environ['myemailaddy'] = [value]

These are brought into the envionment by helpyer.py:
exec(open('$HOME/$PATH/path.py').read())

--- ENDPOINT HELP ---
<klines>
  [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore
  ]
</klines>