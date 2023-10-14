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


    def detect_anomalies(self, transactions):
        message = f"Explain what is happening in this transaction: {transactions}"
        response = self.initiate_chat(message)
        return response

    def initiate_chat(self, message):
        self.user_proxy.initiate_chat(self.assistant, message=message)
        return autogen.ChatCompletion.logged_history

# Output from transactions goes here
initial_prompt = """

"""

def main():
    agent = AnomalyDetectionAgent()
    agent.initiate_chat(initial_prompt)

if __name__ == "__main__":
    main()
