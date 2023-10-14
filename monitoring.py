import time
import requests
safe = '0x171a3ad89cFb7888342f10F4740F72e6F6098A4C'
API_KEY = 'cqt_rQBk7jfGvkByY7TqQBqbHfrBJKKf'

def fetch_transactions():
    url = f'https://api.covalenthq.com/v1/eth-mainnet/address/{safe}/transactions_v3/?key={API_KEY}&with-safe=true&no-logs=true'
    r = requests.get(url)
    data = r.json()
    return data


def detect_anomalies(transactions):
    # Your AI model logic here. Call anomaly_detection_agent
    anomalies = []
    for tx in transactions['data']['items']:
        if is_anomalous(tx):  # Some function that uses your AI model
            anomalies.append(tx)
    return anomalies

def send_alert(anomalies):
    # Your alerting logic here
    for anomaly in anomalies:
        print(anomaly)  # Print anomaly

while True:
    transactions = fetch_transactions()
    anomalies = detect_anomalies(transactions)
    if anomalies:
        send_alert(anomalies)
    time.sleep(60)
