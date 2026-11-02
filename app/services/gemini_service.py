"""
AgriSense - Google Gemini AI Agricultural Assistant Service
Uses the official google-genai Python SDK and python-dotenv.
Reads GEMINI_API_KEY and GEMINI_MODEL (defaults to gemini-3.8-flash).
Injects real-time farm context (weather, soil parameters, ML recommendations).
Handles multi-turn conversations and errors gracefully.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SYSTEM_INSTRUCTION = """
You are the AgriSense Intelligent Agricultural Assistant, an AI agronomic advisor embedded within the AgriSense Decision Support System.

Your core objectives:
1. Provide accurate, clear, and practical agricultural explanations for farmers, agricultural students, and agronomists.
2. Answer questions regarding crop recommendations, soil health (NPK and pH), irrigation strategies, fertilizer scheduling, weather impacts, and crop phenology.
3. Be aware of the active farm context provided with each query (such as current location, real-time weather readings, soil NPK values, and recent crop model predictions).
4. Maintain strict scientific integrity:
   - Never invent or fabricate soil measurements or weather observations.
   - Distinguish actual data from agronomic assumptions.
   - Communicate uncertainty when data is incomplete.
   - Explicitly recommend physical soil testing at certified agricultural laboratories (e.g., Krishi Vigyan Kendra - KVK) before making costly commercial fertilizer investments.
5. Keep answers practical, structured, easy to read, with bullet points and clear sections where helpful.
"""

def get_gemini_client():
    """
    Initializes and returns the google-genai Client if API key is present.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_actual_api_key_here":
        return None, "API key not configured in .env file."
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Failed to initialize Gemini client: {str(e)}"

def format_farm_context(context):
    """
    Constructs a concise context header from current farm state.
    """
    if not context:
        return ""
    
    lines = ["\n[CURRENT AGRISENSE FARM CONTEXT]"]
    if "location" in context and context["location"]:
        loc = context["location"]
        lines.append(f"- Location: {loc.get('name', 'Unknown')} (Lat: {loc.get('latitude', '')}, Lon: {loc.get('longitude', '')})")
    if "weather" in context and context["weather"]:
        w = context["weather"]
        lines.append(f"- Weather: {w.get('temperature', 'N/A')} °C, Humidity: {w.get('humidity', 'N/A')}%, Condition: {w.get('condition', 'N/A')}, Precipitation: {w.get('precipitation', 0)} mm")
    if "soil" in context and context["soil"]:
        s = context["soil"]
        lines.append(f"- Soil Test: N={s.get('nitrogen', 'N/A')} kg/ha, P={s.get('phosphorus', 'N/A')} kg/ha, K={s.get('potassium', 'N/A')} kg/ha, pH={s.get('ph', 'N/A')}")
    if "last_recommendation" in context and context["last_recommendation"]:
        rec = context["last_recommendation"]
        lines.append(f"- Latest Recommended Crop: {rec.get('crop', 'N/A')} (Confidence: {rec.get('confidence', 'N/A')}%)")
    lines.append("[END CONTEXT]\n")
    return "\n".join(lines)

def send_chat_message(message, conversation_history=None, farm_context=None):
    """
    Sends a message to Gemini and returns the AI response.
    Supports multi-turn history and farm context injection.
    """
    if not message or not message.strip():
        return {
            "success": False,
            "error": "Message cannot be empty."
        }

    client, err = get_gemini_client()
    if client is None:
        return {
            "success": False,
            "error": (
                "Gemini API key is not configured. Please open the `.env` file in the project root "
                "and set your actual key:\nGEMINI_API_KEY=your_key_here\n"
                "Then restart the application or refresh this page."
            ),
            "is_config_error": True
        }

    model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    if not model_name:
        model_name = "gemini-3.8-flash"

    try:
        from google.genai import types

        context_header = format_farm_context(farm_context)

        # Assemble prompt with context and history
        contents = []

        if conversation_history and isinstance(conversation_history, list):
            # Include previous turns (limit to last 10 messages for efficiency)
            for item in conversation_history[-10:]:
                role = item.get("role", "user")
                text = item.get("text", "")
                if role == "user":
                    contents.append(types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=text)]
                    ))
                elif role in ["assistant", "model"]:
                    contents.append(types.Content(
                        role="model",
                        parts=[types.Part.from_text(text=text)]
                    ))

        # Add current user prompt with attached context
        user_prompt = f"{context_header}\n{message.strip()}" if context_header else message.strip()
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_prompt)]
        ))

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.3,
            max_output_tokens=1500
        )

        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=config
        )

        reply_text = response.text or "I was unable to generate a response. Please try rephrasing your question."

        return {
            "success": True,
            "reply": reply_text,
            "model": model_name
        }

    except Exception as e:
        error_str = str(e)
        if "API_KEY_INVALID" in error_str or "API key not valid" in error_str:
            user_msg = "The configured Gemini API key is invalid. Please check your GEMINI_API_KEY in .env."
        elif "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
            user_msg = "Gemini API rate limit reached. Please wait a moment before sending another query."
        else:
            user_msg = f"Gemini API request failed: {error_str}"

        return {
            "success": False,
            "error": user_msg
        }
