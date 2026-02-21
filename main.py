from agent.agent_setup import create_agent
from agent.prompts import DAILY_PLAN_PROMPT
from utils.json_parser import parse_agent_output
from agent.memory_manager import load_habits, save_habit
import json

# Initialize agent
agent = create_agent()

# Load previous habits
habit_memory = load_habits()

# User input
user_input = "I exercised yesterday but skipped meditation. Give me today's plan and tips."

# Include prompt for structured output
full_prompt = DAILY_PLAN_PROMPT + "\nUser Input: " + user_input

# Run agent
response = agent.run(full_prompt)

# Parse structured JSON output
parsed = parse_agent_output(response)

if parsed:
    print("Daily Plan:", parsed.daily_plan)
    print("Progress:", parsed.progress)
    print("Tips:", parsed.tips)

    # Save to habit history
    habit_memory["latest"] = {
        "daily_plan": parsed.daily_plan,
        "progress": parsed.progress,
        "tips": parsed.tips
    }
    save_habit(habit_memory)
