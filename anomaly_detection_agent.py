import autogen
import os 
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
config_list = [
    {
        'model': 'gpt-3.5-turbo',
        'api_key': OPEN_API_KEY,
    },  ]

class AnomalyDetectionAgent:
    def __init__(self):
        self.assistant = autogen.AssistantAgent(
            name="assistant",
            llm_config={
                "seed": 41,
                "config_list": config_list,
            }
        )
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="ALWAYS",
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        )

    def is_anomalous(self, tx):
        # Your anomaly detection logic here
        # Use the AI model to determine if the transaction is anomalous
        # Return True if anomalous, False otherwise
        return False

    def detect_anomalies(self, transactions):
        anomalies = []
        for tx in transactions['data']['items']:
            if self.is_anomalous(tx):
                anomalies.append(tx)
        return anomalies

    def initiate_chat(self, message):
        self.user_proxy.initiate_chat(self.assistant, message=message)
        return autogen.ChatCompletion.logged_history

# Output from transactions goes here
initial_prompt = """

"""

agent = AnomalyDetectionAgent()
agent.initiate_chat(initial_prompt)
