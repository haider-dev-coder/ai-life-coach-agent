import json
import re
from types import SimpleNamespace

def parse_agent_output(text: str):
    try:
        # Find JSON object between curly braces
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        
        if json_match:
            json_str = json_match.group()
            data = json.loads(json_str)
            
            # Ensure all required fields exist
            result = {
                'daily_plan': data.get('daily_plan', []),
                'progress': data.get('progress', []),
                'tips': data.get('tips', [])
            }
            
            return SimpleNamespace(**result)
        else:
            print("No JSON found in response")
            return None
        
    except Exception as e:
        print(f"Parse Error: {e}")
        return None