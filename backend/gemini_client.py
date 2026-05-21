import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env variables
load_dotenv()

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("GEMINI_API_KEY missing in .env")


# Configure Gemini
genai.configure(api_key=API_KEY)


# Initialize model
try:
    model = genai.GenerativeModel(
        model_name="gemini-3.5-flash"
    )

    print("Gemini model initialized successfully")

except Exception as e:
    print("Model initialization error:", e)
    model = None


def ask_gemini(prompt: str) -> str:
    """
    Send prompt to Gemini and return text response
    """

    try:

        if model is None:
            raise Exception(
                "Gemini model unavailable"
            )

        response = model.generate_content(
            prompt
        )

        # safer extraction
        text = getattr(
            response,
            "text",
            ""
        )

        if not text:
            raise Exception(
                "Empty Gemini response"
            )

        print("\n===== GEMINI RAW RESPONSE =====")
        print(text)
        print("================================\n")

        return text.strip()

    except Exception as e:

        print(
            "Gemini Error:",
            str(e)
        )

        return ""