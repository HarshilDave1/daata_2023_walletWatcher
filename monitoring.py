import time
import requests
import anomaly_detection_agent

safe = '0x171a3ad89cFb7888342f10F4740F72e6F6098A4C'
API_KEY = 'cqt_rQBk7jfGvkByY7TqQBqbHfrBJKKf'

def fetch_transactions():
    url = f'https://api.covalenthq.com/v1/eth-mainnet/address/{safe}/transactions_v3/?key={API_KEY}&with-safe=true&no-logs=true'
    r = requests.get(url)
    data = r.json()
    return data


def detect_anomalies(transactions):
    anomalies = []
    for tx in transactions['data']['items']:
        if anomaly_detection_agent.is_anomalous(tx):  # Call anomaly_detection_agent.is_anomalous function
            anomalies.append(tx)
    return anomalies

def send_alert(anomalies):
    for anomaly in anomalies:
        print(anomaly)

while True:
    transactions = fetch_transactions()
    anomalies = detect_anomalies(transactions)
    if anomalies:
        send_alert(anomalies)
    time.sleep(60)
