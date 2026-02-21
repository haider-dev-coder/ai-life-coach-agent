import google.generativeai as genai
from langchain_core.tools import Tool
from tools.sentiment_tool import sentiment_analyzer
from tools.reminder_tool import set_reminder
from tools.calendar_tool import add_to_calendar
from config import GEMINI_API_KEY, MODEL_NAME
from agent import prompts

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Define tools
tools = [sentiment_analyzer, set_reminder, add_to_calendar]

# Simple agent executor
class SimpleAgent:
    def __init__(self, model_name,prompts, tools):
        self.model = genai.GenerativeModel(model_name)
        self.tools = tools
        self.prompts = prompts
    
    def invoke(self, inputs):
        user_input = inputs["input"]
        response = self.model.generate_content(user_input)
        return {"output": response.text}

agent_executor = SimpleAgent(MODEL_NAME, tools, prompts)