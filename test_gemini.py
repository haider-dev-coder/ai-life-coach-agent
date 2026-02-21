import google.generativeai as genai

genai.configure(api_key="AIzaSyAcYsno-6IPniuuXFGlMbuYb1xaQXffUsU")

print("Available models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")