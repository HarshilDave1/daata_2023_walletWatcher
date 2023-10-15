from sklearn.ensemble import IsolationForest
import sqlite3

class AnalyzerAgent:
    def __init__(self):
        self.model = None

    def fetch_data(self):
        conn = sqlite3.connect('transactions.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT tx_hash,from_address, to_address, value, gas_spent, fees_paid, block_signed_at FROM transactions')
        data = cursor.fetchall()
        conn.close()
        return data


    def engineer_features(self, transactions):
        # Extracting individual fields for easier processing
        to_addresses = [tx[1] for tx in transactions]
        from_addresses = [tx[2] for tx in transactions]
        values = [tx[3] for tx in transactions]
        gas_spents = [tx[4] for tx in transactions]
        fees_paids = [tx[5] for tx in transactions]
        times = [int(tx[6].split('T')[1].split(':')[0]) for tx in transactions]  # Extracting hour from the timestamp

        # Feature: to_address frequency
        to_address_freq = [to_addresses.count(addr) for addr in to_addresses]

        # Feature: from_address frequency
        from_address_freq = [from_addresses.count(addr) for addr in from_addresses]

        # Feature: unusual time (1 if transaction time is between 12 AM to 5 AM, else 0)
        unusual_times = [1 if 0 <= time <= 5 else 0 for time in times]

        # Combining all features into a single dataset
        features = list(zip(values, gas_spents, fees_paids, to_address_freq, from_address_freq, unusual_times))
        
        return features


    def train(self, data):
        self.model = IsolationForest(contamination=0.001)  # Assuming 0% of the data is considered as anomalies
        self.model.fit(data)

    def predict(self, transaction):
        # Engineer features for the new transaction
        features = self.engineer_features([transaction])
        return self.model.predict(features)[0] == -1  # -1 indicates anomaly

    def retrain(self):
        data = self.fetch_data()
        features = self.engineer_features(data)
        self.train(features)

# Run training
def main():
    analyzer = AnalyzerAgent()
    analyzer.retrain()  # Initial training

if __name__ == "__main__":
    main()



# For each new transaction:
# transaction = {
#     # ... (transaction details)
# }
# if analyzer.predict(transaction):
#     print("Anomalous transaction detected!")
