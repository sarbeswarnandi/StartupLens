import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env variables
load_dotenv()

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("GEMINI_API_KEY missing in .env file")


# Configure Gemini SDK
genai.configure(api_key=API_KEY)


# Initialize model
try:
    # Set to the stable high-efficiency Gemini 3.1 Flash-Lite engine
    model = genai.GenerativeModel(
        model_name="gemini-3.1-flash-lite"
    )
    print("Gemini model (gemini-3.1-flash-lite) initialized successfully")

except Exception as e:
    print("Model initialization error:", e)
    model = None


def ask_gemini(prompt: str) -> str:
    """
    Send prompt to Gemini 3.1 Flash-Lite and return text response
    """
    try:
        if model is None:
            raise Exception("Gemini model unavailable")

        # Call the Gemini API 
        response = model.generate_content(prompt)

        # Safe response extraction
        text = getattr(response, "text", "")

        if not text:
            # Check for safety filter interruptions
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                print("Prompt blocked by safety filters:", response.prompt_feedback)
            raise Exception("Empty Gemini response")

        print("\n===== GEMINI RAW RESPONSE =====")
        print(text)
        print("================================\n")

        return text.strip()

    except Exception as e:
        print("Gemini Error:", str(e))
        return ""


# Self-test code snippet to test execution directly 
if __name__ == "__main__":
    print("Running a test call to Gemini...")
    test_prompt = "Hello! Confirm that you are running on the Gemini 3.1 Flash-Lite engine."
    ask_gemini(test_prompt)