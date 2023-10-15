import sqlite3
import smtplib
from email.message import EmailMessage
from IPython import get_ipython

def exec_python(cell):
    ipython = get_ipython()
    result = ipython.run_cell(cell)
    log = str(result.result)
    if result.error_before_exec is not None:
        log += f"\n{result.error_before_exec}"
    if result.error_in_exec is not None:
        log += f"\n{result.error_in_exec}"
    return log

# Define the function for the Analyzer Agent
def analyze_transaction():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions ORDER BY tx_hash DESC LIMIT 1')
    transaction = cursor.fetchone()
    conn.close()
    # Analyze the transaction and return details
    return transaction

# Define the function for the Notifier Agent
def notify_user(transaction):
    msg = EmailMessage()
    msg.set_content(str(transaction))
    msg['Subject'] = 'High-risk Transaction Alert'
    msg['From'] = 'sender_email@example.com'
    msg['To'] = 'receiver_email@example.com'
    # Send the email
    # with smtplib.SMTP('smtp.example.com') as s:
    #     s.send_message(msg)
    print(msg)

# Define the function for the Guardian Agent
def move_funds(private_key):
    # Logic to move funds using the private key
    pass

# Define the function for the Planner Agent
def get_user_feedback():
    feedback = input("Please provide your feedback: ")
    return feedback


functions = [
    {
            "name": "python",
            "description": "run cell in ipython and return the execution result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cell": {
                        "type": "string",
                        "description": "Valid Python cell to execute.",
                    }
                },
                "required": ["cell"],
            },
        },
    {
        "name": "analyze_transaction",
        "description": "Access the database and read the latest transaction information.",
        "parameters": {
            "type": "object",  # Specify the type as "object"
            "properties": {}  # Specify an empty properties object
        }
    },
    {
        "name": "notify_user",
        "description": "Email the user with transaction details.",
        "parameters": {
            "type": "object",
            "properties": {
                "transaction": {
                    "type": "string",
                    "description": "Transaction details to notify the user about.",
                    
                }
            },
            "required": ["transaction"],
        },
    },
    {
        "name": "move_funds",
        "description": "Move funds to a predetermined wallet.",
        "parameters": {
            "type": "object",
            "properties": {
                "private_key": {
                    "type": "string",
                    "description": "Private key to authorize the fund transfer.",
                }
            },
            "required": ["private_key"],
        },
    },
        {
        "name": "analyze_transaction",
        "description": "Access the database and read the latest transaction information.",
        "parameters": {
            "type": "object",  # Specify the type as "object"
            "properties": {}  # Specify an empty properties object
        }
    },
]

