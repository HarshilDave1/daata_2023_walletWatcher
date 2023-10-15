from flask import Flask, request, jsonify, render_template
import monitoring

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_detection():
    safe_address = request.form.get('safe_address')
    # Set the safe address in your monitoring module
    monitoring.safe = safe_address
    anomalies = monitoring.detect_anomalies()
    return jsonify(anomalies)

if __name__ == '__main__':
    app.run(debug=True)
