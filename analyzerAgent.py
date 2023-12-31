from sklearn.ensemble import IsolationForest
import sqlite3
import joblib

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
    def fetch_latest_data(self):
        conn = sqlite3.connect('transactions.db')
        cursor = conn.cursor()
        
        # Fetch the latest 100 transactions ordered by block_signed_at in descending order
        cursor.execute('''
        SELECT tx_hash, from_address, to_address, value, gas_spent, fees_paid, block_signed_at 
        FROM transactions 
        ORDER BY block_signed_at DESC 
        LIMIT 100
        ''')
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

    def predict(self):
        # Fetch the latest 100 transactions from the database
        latest_transactions = self.fetch_latest_data()
        
        anomalies = []
        for tx in latest_transactions:
            # Engineer features for the transaction
            features = self.engineer_features([tx])
            
            # Get the anomaly score
            anomaly_score = self.model.decision_function(features)[0]
            
            # Check if the transaction is an anomaly
            is_anomaly = self.model.predict(features)[0] == -1  # -1 indicates anomaly
            
            if is_anomaly:
                # Convert the transaction tuple to a dictionary with labels
                tx_dict = {
                    "tx_hash": tx[0],
                    "from_address": tx[1],
                    "to_address": tx[2],
                    "value": tx[3],
                    "gas_spent": tx[4],
                    "fees_paid": tx[5],
                    "block_signed_at": tx[6],
                    "anomaly_score": anomaly_score
                }
                anomalies.append(tx_dict)
        
        # Sort anomalies by their scores to see the most anomalous transactions first
        anomalies.sort(key=lambda x: x["anomaly_score"])
        
        return anomalies




    def retrain(self):
        data = self.fetch_data()
        features = self.engineer_features(data)
        self.train(features)
        self.save_model()
        
    def save_model(self, filename="trained_model.pkl"):
        """Save the trained model to a file."""
        joblib.dump(self.model, filename)

    def load_model(self, filename="trained_model.pkl"):
        """Load a pretrained model from a file."""
        self.model = joblib.load(filename)


# Run training
def main():
    analyzer = AnalyzerAgent()
    # Check if a pretrained model exists and load it
    try:
        analyzer.load_model()
        print("Loaded pretrained model.")
    except:
        print("No pretrained model found. Training a new model...")
        analyzer.retrain()  # Initial training

if __name__ == "__main__":
    main()



# For each new transaction:
# transaction = {
#     # ... (transaction details)
# }
# if analyzer.predict(transaction):
#     print("Anomalous transaction detected!")
