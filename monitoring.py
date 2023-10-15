import time
import requests
from monitoring_agents2 import AnomalyDetectionAgent
from dotenv import load_dotenv
import os
from database import insert_transaction, transaction_exists
load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
safe = '0x31d7a5194fe60ac209cf1ce2d539c9a60662ed6b'
Covalent_API_KEY = os.getenv("Covalent_API_KEY")
chain = 'avalanche-mainnet' # for mainnet

def fetch_transactions():
    page = 0 #only get the latest transactions
    url = f'https://api.covalenthq.com/v1/{chain}/address/{safe}/transactions_v3/page/{page}/?key={Covalent_API_KEY}&no-logs=true&with-safe=true'
    r = requests.get(url)
    data = r.json()
    # Save transactions into the database
    for tx in data['data']['items']:
        insert_transaction(tx)  
            
    return data



def fetch_old_transactions():
    page = 0  
    while True:  
        url = f'https://api.covalenthq.com/v1/{chain}/address/{safe}/transactions_v3/page/{page}/?key={Covalent_API_KEY}&no-logs=true&with-safe=true'
        r = requests.get(url)
        data = r.json()
        
        # Check if the transactions list is empty
        if not data['data']['items']:
            break  # Exit the loop if there are no more transactions
        
        # Save transactions into the database
        for tx in data['data']['items']:
            insert_transaction(tx)  
        
        page += 1  

    return data



def detect_anomalies(transactions):
    anomalies = []
    agent = AnomalyDetectionAgent()
    for tx in transactions['data']['items']:
        if not transaction_exists(tx['tx_hash']):
            if agent.detect_anomalies(tx):
                anomalies.append(tx)
            insert_transaction(tx)
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
