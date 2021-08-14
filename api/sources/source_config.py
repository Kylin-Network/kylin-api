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
  cryptowatch = dict(
    source_name = "cryptowatch",
    url = "https://api.cryptowat.ch/markets/prices",
  ),
  bancor = dict(
    source_name = "bancor",
    url = "https://api-v2.bancor.network/tokens",
  ),
  kraken = dict(
    source_name = "kraken",
    url = "https://api.cryptowat.ch/markets/kraken/FROM_CURRENCYTO_CURRENCY/price",
  ),
 bitfinex = dict(
    source_name = "bitfinex",
    url = "https://api.cryptowat.ch/markets/bitfinex/FROM_CURRENCYTO_CURRENCY/price",
  ),
 binance = dict(
    source_name = "binance",
    url = "https://api.binance.com/api/v3/ticker/price?symbol=FROM_CURRENCYTO_CURRENCY",
  ),
)
