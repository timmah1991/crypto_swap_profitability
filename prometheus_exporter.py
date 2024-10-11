import requests, json
from prometheus_client import Gauge, generate_latest, REGISTRY
from prometheus_client.core import CollectorRegistry
from prometheus_client import MetricsHandler
from http.server import BaseHTTPRequestHandler, HTTPServer

tradeables = ["LTC", "ETH", "XRP", "DOGE", "USDT"]

crypto_trade_routes = Gauge('crypto_trade_routes', 'Trade routes and profitability by type', ['pair'])

def fetch_btc_to_eth_conversion_rate():
    rawdata = requests.get('https://api.coingate.com/v2/rates').json()
    valuablepairs = {}

    for firsthop in tradeables:
        for secondhop in tradeables:
            if secondhop == firsthop: continue
            priceindex2 = 1.0
            priceindex2 = priceindex2 * float(rawdata["merchant"]["BTC"][firsthop]) * float(rawdata["merchant"][firsthop][secondhop]) * float(rawdata["merchant"][secondhop]["BTC"])
            valuablepairs[str("BTC_" + firsthop + "_" + secondhop + "_BTC")] = priceindex2
            for thirdhop in tradeables:
                if((thirdhop == firsthop) or (thirdhop == secondhop)): continue
                priceindex3 = 1.0
                priceindex3 = priceindex3 * float(rawdata["merchant"]["BTC"][firsthop]) * float(rawdata["merchant"][firsthop][secondhop]) * float(rawdata["merchant"][secondhop][thirdhop]) * float(rawdata["merchant"][thirdhop]["BTC"])
                valuablepairs[str("BTC_" + firsthop + "_" + secondhop + "_" + thirdhop + "_BTC")] = priceindex3
                for fourthhop in tradeables:
                    if((fourthhop == firsthop) or (fourthhop == secondhop) or (fourthhop == thirdhop)): continue
                    priceindex4 = 1.0
                    priceindex4 = priceindex4 * float(rawdata["merchant"]["BTC"][firsthop]) * float(rawdata["merchant"][firsthop][secondhop]) * float(rawdata["merchant"][secondhop][thirdhop]) * float(rawdata["merchant"][thirdhop][fourthhop]) * float(rawdata["merchant"][fourthhop]["BTC"])
                    valuablepairs[str("BTC_" + firsthop + "_" + secondhop + "_" + thirdhop + "_" + fourthhop + "_BTC")] = priceindex4
                    
    for pairdata in list(valuablepairs.keys()):
        crypto_trade_routes.labels(pair=pairdata).set(valuablepairs.get(pairdata))

class CustomMetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handles GET requests for Prometheus scraping."""
        # Fetch the latest BTC to ETH conversion rate
        fetch_btc_to_eth_conversion_rate()
        
        # Set HTTP response headers
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
        self.end_headers()
        
        # Output the latest metrics to the HTTP response
        output = generate_latest(REGISTRY)
        self.wfile.write(output)

if __name__ == "__main__":
    # Start an HTTP server to serve the metrics on port 8069
    server = HTTPServer(('0.0.0.0', 8069), CustomMetricsHandler)
    print("Starting server on port 8069...")
    server.serve_forever()