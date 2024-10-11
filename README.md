Crypto Trade Routes Profiler - README


This project is designed to track profitable cryptocurrency trading routes using data from the CoinGate API. It focuses on calculating potential conversion rates for multiple cryptocurrencies, specifically LTC, ETH, XRP, DOGE, and USDT, and makes the data available for Prometheus monitoring.

The tool performs multi-hop crypto-to-crypto conversion rate calculations, tracking profitable routes involving Bitcoin (BTC) as the base currency. The results are exposed as metrics, which can be scraped by Prometheus to monitor in real-time.

Features
Fetches real-time conversion rates from the CoinGate API.
Calculates profitable trade routes through up to four "hops" between different cryptocurrencies.
Exposes the results as Prometheus-compatible metrics.
Runs an HTTP server that Prometheus can scrape to collect the data.
Prerequisites
Python 3.x
Required Python libraries:
requests (to fetch data from CoinGate)
prometheus_client (to expose the metrics)
CoinGate API access (no API key needed for public rates)
You can install the required libraries using the following command:

bash
Copy code
pip install requests prometheus-client
How It Works
Tradeables: The code considers a set of cryptocurrencies (LTC, ETH, XRP, DOGE, USDT) for potential trading routes starting and ending with BTC.
Conversion Rate Calculation:
The code fetches conversion rates from the CoinGate API.
It computes conversion routes using multiple cryptocurrencies, calculating the total value when converting back to BTC after up to four "hops."
Prometheus Metrics Exposure:
Trade routes are stored in a Gauge metric with Prometheus.
Metrics are exposed via an HTTP server on port 8069, which Prometheus can scrape.
Key Code Components
fetch_btc_to_eth_conversion_rate():

Fetches data from the CoinGate API.
Calculates profitable conversion routes between BTC and the selected tradeable cryptocurrencies.
Updates the Prometheus gauge with the results.
CustomMetricsHandler:

A custom HTTP handler that exposes the calculated metrics for Prometheus.
HTTP Server:

A simple HTTP server that runs on port 8069, allowing Prometheus to scrape the exposed metrics.
How to Run
Install the necessary dependencies using pip.
Run the Python script:
bash
Copy code
python crypto_trade_routes.py
The server will start on 0.0.0.0:8069 and expose the metrics to Prometheus.
Metrics
The metrics are exposed in Prometheus format and include:

crypto_trade_routes{pair="BTC_LTC_XRP_BTC"}: This represents a specific trading route starting and ending with BTC, with intermediary hops through LTC and XRP.
Prometheus Configuration
To scrape the metrics with Prometheus, add the following job to your prometheus.yml configuration:

yaml
Copy code
scrape_configs:
  - job_name: 'crypto_trade_routes'
    static_configs:
      - targets: ['<server_ip>:8069']
Replace <server_ip> with the IP address of the machine running the script.

License
This project is open-source and available under the MIT License.

Feel free to modify this script for additional cryptocurrencies or trade routes!