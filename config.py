"""
KachraGrid v2 - Configuration
Bangalore Ward 142 (Jayanagar) Constants & Settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Paths
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
DB_PATH = Path(os.getenv("DATABASE_URL", str(DATA_DIR / "kachragrid.db")).replace("sqlite:///", ""))

DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Ward Information
CITY_NAME = os.getenv("CITY_NAME", "Bangalore")
WARD_NUMBER = os.getenv("WARD_NUMBER", "142")
WARD_NAME = os.getenv("WARD_NAME", "Jayanagar")
WARD_CENTER_LAT = float(os.getenv("WARD_CENTER_LAT", 12.9250))
WARD_CENTER_LON = float(os.getenv("WARD_CENTER_LON", 77.5830))

# Fuel & Logistics Parameters
DIESEL_RATE_PER_LITER = float(os.getenv("DIESEL_RATE_PER_LITER", 89.0))  # ₹89/liter in Bangalore
TRUCK_SPECS = {
    "T01": {"driver": "Rajesh Kumar", "mileage": 6.0, "capacity_kg": 5000, "plate": "KA-01-EA-1042"},
    "T02": {"driver": "Suresh Reddy", "mileage": 5.5, "capacity_kg": 4500, "plate": "KA-01-EA-2091"},
    "T03": {"driver": "Manjunath", "mileage": 7.0, "capacity_kg": 4000, "plate": "KA-01-EA-3184"},
}

# Old traditional fixed route distance per day (for savings baseline)
TRADITIONAL_FIXED_ROUTE_KM = float(os.getenv("TRADITIONAL_FIXED_ROUTE_KM", 32.5))

# Hugging Face Model Repositories
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_TEXT_MODEL = os.getenv("HF_TEXT_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
HF_VISION_MODEL = os.getenv("HF_VISION_MODEL", "Qwen/Qwen2.5-VL-7B-Instruct")
HF_VOICE_MODEL = os.getenv("HF_VOICE_MODEL", "openai/whisper-small")
HF_TRANSLATION_MODEL = os.getenv("HF_TRANSLATION_MODEL", "facebook/nllb-200-distilled-600M")

# AI Inference Mode
default_device = "mps" if os.uname().sysname == "Darwin" else "cpu"
HF_DEVICE = os.getenv("HF_DEVICE", default_device)
AI_OFFLINE_FAST_MODE = os.getenv("AI_OFFLINE_FAST_MODE", "true").lower() in ("true", "1", "yes")

# Optional Cloud & Mapping Keys
CARTO_API_KEY = os.getenv("CARTO_API_KEY", "")
CARTO_USERNAME = os.getenv("CARTO_USERNAME", "")
# Optional Cloud AI & OpenRouter
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_VISION_MODEL = os.getenv("OPENROUTER_VISION_MODEL", "openrouter/free")
MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN", "")
OPENROUTE_SERVICE_API_KEY = os.getenv("OPENROUTE_SERVICE_API_KEY", "")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "")
