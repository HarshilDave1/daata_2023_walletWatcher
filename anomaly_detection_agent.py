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



# create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "seed": 41,
        "config_list": config_list,
    }
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)

# the purpose of the following line is to log the conversation history
autogen.ChatCompletion.start_logging()

# Output from transactions goes here
initial_prompt = """

"""

# the assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(assistant, message=initial_prompt)

print(autogen.ChatCompletion.logged_history)