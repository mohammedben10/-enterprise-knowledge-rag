"""
Google Gemini API Health Check
------------------------------
Verifies that your Google Gemini API key is valid and can generate a response.
"""

import os
from dotenv import load_dotenv
from google import genai
import config

load_dotenv()


def test_gemini_connection():
    print("=" * 60)
    print("🤖 Checking Google Gemini API Connectivity...")
    print("=" * 60)

    api_key = config.GOOGLE_API_KEY
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY is not set in your .env file.")
        return False

    masked = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
    print(f"🔑 Detected API Key: {masked}")
    print(f"⚡ Testing Model: {config.GEMINI_MODEL}")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents="Reply in one short sentence: System is operational."
        )
        print(f"\n✅ Connection Successful! Response from Gemini:\n   \"{response.text.strip()}\"")
        print("=" * 60 + "\n")
        return True
    except Exception as e:
        print(f"\n❌ Gemini API Error: {e}")
        return False


if __name__ == "__main__":
    test_gemini_connection()
