import autogen
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
config_list = {
    "seed": 42,
    "temperature": 0,
    'model': 'gpt-3.5-turbo',
    "request_timeout": 120,
    'api_key': OPEN_API_KEY,
}

class AnomalyDetectionAgent:
    def __init__(self):
        # Monitor Agent
        self.monitor = autogen.AssistantAgent(
            name="Monitor",
            llm_config=config_list,
            system_message="Monitors the user's wallet for any transactions. Reports transactions in real-time."
        )
        
        # Analyzer Agent
        self.analyzer = autogen.AssistantAgent(
            name="Analyzer",
            llm_config=config_list,
            system_message="Analyzes transactions for potential risks. Uses AI and predefined rules to assess transaction safety."
        )
        
        # Notifier Agent
        self.notifier = autogen.AssistantAgent(
            name="Notifier",
            llm_config=config_list,
            system_message="Responsible for notifying the user about high-risk transactions. Provides details and seeks user input if necessary."
        )
        
        # Guardian Agent
        self.guardian = autogen.AssistantAgent(
            name="Guardian",
            llm_config=config_list,
            system_message="Takes protective actions in case of high-risk transactions. Acts based on predefined rules or user input."
        )
        
        # User Proxy Agent
        self.user_proxy = autogen.UserProxyAgent(
            name="User Proxy",
            system_message="Represents the user. Receives alerts and provides feedback or directives to other agents.",
            human_input_mode="ALWAYS",
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        )
        
        # Auditor Agent
        self.auditor = autogen.AssistantAgent(
            name="Auditor",
            llm_config=config_list,
            system_message="Reviews the system's performance. Ensures accuracy and reliability."
        )
        
        # Planner Agent
        self.planner = autogen.AssistantAgent(
            name="Planner",
            llm_config=config_list,
            system_message="Refines the system's strategy. Updates rules and heuristics based on feedback."
        )
        
        # Critic Agent
        self.critic = autogen.AssistantAgent(
            name="Critic",
            llm_config=config_list,
            system_message="Double checks plans, claims, and actions. Provides feedback to ensure accuracy and reliability."
        )
        
        # Group Chat for the agents
        self.groupchat = autogen.GroupChat(
            agents=[self.monitor, self.analyzer, self.notifier, self.guardian, self.user_proxy, self.auditor, self.planner, self.critic],
            messages=[],
            max_round=50
        )
        
        # Manager for the group chat
        self.manager = autogen.GroupChatManager(groupchat=self.groupchat, llm_config=config_list)

    def detect_anomalies(self, transactions):
        message = f"""
        Monitor: Please provide details of the latest transactions for the user's wallet.
        Analyzer: Assess these transactions for potential risks using AI models and predefined rules.
        Notifier: If any high-risk transactions are detected, alert the User Proxy with details.
        Guardian: Based on the risk assessment, suggest protective actions if necessary.
        User Proxy: Please review any alerts and provide feedback or directives.
        Auditor: Periodically review the actions taken and provide feedback.
        Planner: Refine the strategy based on feedback from the Auditor and User Proxy.
        Critic: Ensure all agents are functioning correctly and provide feedback where necessary.

        Current Transaction Details: {transactions}
        """
        response = self.initiate_chat(message)
        return response

    def initiate_chat(self, message):
        self.user_proxy.initiate_chat(self.monitor, message=message)
        return autogen.ChatCompletion.logged_history


initial_prompt = """
Get Hello World response from all agents
"""

def main():
    agent = AnomalyDetectionAgent()
    agent.initiate_chat(initial_prompt)

if __name__ == "__main__":
    main()

