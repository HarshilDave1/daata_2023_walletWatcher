import time
import requests
import anomaly_detection_agent
from dotenv import load_dotenv
import os
load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
safe = '0x171a3ad89cFb7888342f10F4740F72e6F6098A4C'
Covalent_API_KEY = os.getenv("Covalent_API_KEY")
chain = 'avalanche-mainnet' # for mainnet

def fetch_transactions():
    url = f'https://api.covalenthq.com/v1/{chain}/address/{safe}/transactions_v3/?key={Covalent_API_KEY}&with-safe=true&no-logs=true'
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

def main():
    while True:
        transactions = fetch_transactions()
        anomalies = detect_anomalies(transactions)
        if anomalies:
            send_alert(anomalies)
        time.sleep(60)

if __name__ == "__main__":
    main()
