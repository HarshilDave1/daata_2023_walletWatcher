import time
import requests
from monitoring_agents2 import AnomalyDetectionAgent
from dotenv import load_dotenv
import os
load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
safe = '0x31d7a5194fe60ac209cf1ce2d539c9a60662ed6b'
Covalent_API_KEY = os.getenv("Covalent_API_KEY")
chain = 'avalanche-mainnet' # for mainnet

def fetch_transactions():
    url = f'https://api.covalenthq.com/v1/{chain}/address/{safe}/transactions_v3/?key={Covalent_API_KEY}&with-safe=true&no-logs=true'
    r = requests.get(url)
    data = r.json()
    return data


def detect_anomalies(transactions):
    anomalies = []
    agent = AnomalyDetectionAgent()  
    for tx in transactions['data']['items']:
        if agent.detect_anomalies(tx):  
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
