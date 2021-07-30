sources = dict(
  coinbase = dict(
    source_name = "coinbase",
    url = "https://api.pro.coinbase.com/products/FROM_CURRENCY-TO_CURRENCY/ticker",
  ),
  coingecko = dict(
    source_name = "coingecko",
    url = "https://api.coingecko.com/api/v3/simple/price?ids=FROM_CURRENCY&vs_currencies=TO_CURRENCY",
  ),
  cryptocompare = dict(
    source_name = "cryptocompare",
    url = "https://min-api.cryptocompare.com/data/price?fsym=FROM_CURRENCY&tsyms=TO_CURRENCY",
  ),
  binance = dict(
    source_name = "cryptocompare",
    url = "https://api.binance.com/api/v3/ticker/price?symbol=FROM_CURRENCYTO_CURRENCY",
  ),
  cryptowatch = dict(
    source_name = "cryptowatch",
    url = "https://api.cryptowat.ch/markets/prices",
  ),
)