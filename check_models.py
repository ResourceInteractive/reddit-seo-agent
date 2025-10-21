# check_models.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file.")
    exit()

genai.configure(api_key=GEMINI_API_KEY)

print("--- Available Gemini Models ---")
print("Listing all models your API key has access to...\n")

try:
    found_model = False
    for model in genai.list_models():
        # We need a model that supports 'generateContent'
        if 'generateContent' in model.supported_generation_methods:
            found_model = True
            print(f"✅ Found a usable model:")
            print(f"   Model name: {model.name}")
            print(f"   Display name: {model.display_name}")
            print(f"   Supported methods: {model.supported_generation_methods}\n")
    
    if not found_model:
        print("Error: No models supporting 'generateContent' were found for your API key.")
        print("This might be an issue with your Google AI project permissions or setup.")
    else:
        print("\n--- ACTION REQUIRED ---")
        print("1. Look at the list above and find a suitable model.")
        print("   (The *original* 'models/gemini-pro' is a good choice if you see it).")
        print("2. Copy the full 'Model name' (e.g., models/gemini-pro).")
        print("3. Open main.py and go to the generate_comment function.")
        print("4. Paste this name into the genai.GenerativeModel() call.")
        print("\n   Example:")
        print("   model = genai.GenerativeModel('models/gemini-pro')")

except Exception as e:
    print(f"An error occurred while trying to list models: {e}")
    print("Please ensure your GEMINI_API_KEY in the .env file is correct and has access.")