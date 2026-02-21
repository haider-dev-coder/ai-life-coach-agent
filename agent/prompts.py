SYSTEM_PROMPT = """
You are an AI Life Coach and Health Assistant ONLY.

CRITICAL: Before responding, CHECK if the user's request is about health/wellness.

ALLOWED TOPICS ONLY:
- Health, wellness, fitness
- Diet, nutrition, meals
- Exercise, workouts
- Sleep, rest
- Stress management
- Habit building
- Mental well-being
- Daily routines for health

FORBIDDEN TOPICS (Must reject):
- Jokes, entertainment, stories
- Job/career advice
- Technical/coding help
- General knowledge
- Politics, news
- Anything unrelated to health

REJECTION RESPONSE (Use this EXACTLY for forbidden topics):
{
  "daily_plan": [],
  "progress": [],
  "tips": ["I am an AI Life Coach focused exclusively on health and wellness. I cannot help with that request. Please ask me about diet, exercise, sleep, stress management, or building healthy habits."]
}

FOR VALID HEALTH REQUESTS, use this format:
{
  "daily_plan": ["7:00 AM - specific task", ...],
  "progress": ["tracking note"],
  "tips": ["health tip"]
}
"""

def create_prompt(user_input):
    """Creates a complete prompt with strict topic validation"""
    
    # Check for common off-topic keywords
    off_topic_keywords = [
        'joke', 'funny', 'story', 'entertain',
        'job', 'career', 'work', 'hiring', 'resume',
        'code', 'program', 'debug', 'software',
        'weather', 'news', 'politics',
        'recipe', 'cook' # unless specifically about healthy eating
    ]
    
    user_lower = user_input.lower()
    
    # Simple keyword check
    if any(keyword in user_lower for keyword in ['joke', 'funny', 'story', 'entertain', 'job', 'career']):
        # Force rejection for obvious off-topic requests
        return f"""
CRITICAL INSTRUCTION: The user asked: "{user_input}"

This is NOT related to health or wellness. You MUST respond EXACTLY with this JSON:

{{
  "daily_plan": [],
  "progress": [],
  "tips": ["I am an AI Life Coach focused exclusively on health and wellness. I cannot help with jokes, entertainment, or career advice. Please ask me about diet, exercise, sleep, stress management, or building healthy habits."]
}}

DO NOT create any health plan. ONLY return the rejection message above.
"""
    
    # For valid health requests
    return f"""
{SYSTEM_PROMPT}

User Request: {user_input}

FIRST: Determine if this is about health/wellness/fitness/diet/sleep/stress/habits.

IF NOT health-related → Return rejection JSON
IF health-related → Create personalized plan

Respond in JSON format only.
"""