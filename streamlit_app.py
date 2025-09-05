# streamlit_app.py
import streamlit as st
import os
from dotenv import load_dotenv
import logging
import traceback

# Load .env for local dev
load_dotenv()

# Configure logging (Streamlit shows logs in "Manage app" → Logs)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

def get_secret(key):
    """Try Streamlit Secrets first, then environment variables."""
    return st.secrets.get(key) if "secrets" in dir(st) and st.secrets.get(key) else os.getenv(key)

# List of keys your app may need
API_KEYS = {
    "GROQ_API_KEY": None,
    "GOOGLE_API_KEY": None,
    "GEOAPIFY_API_KEY": None,
    "FOURSQUARE_API_KEY": None,
    "TAVILAY_API_KEY": None,
    "OPENWEATHERMAP_API_KEY": None,
    "EXCHANGE_RATE_API_KEY": None,
}

# Populate from secrets/env
for k in API_KEYS.keys():
    API_KEYS[k] = get_secret(k)

# Display or block if required keys missing
required = ["GOOGLE_API_KEY", "TAVILAY_API_KEY"]  # adjust required keys for your app
missing_required = [k for k in required if not API_KEYS.get(k)]

if missing_required:
    st.title("AI Travel Planner")
    st.error(
        "Missing required API key(s): "
        + ", ".join(missing_required)
        + ".\n\nAdd them in Streamlit > Manage app > Settings > Secrets (TOML), or add locally to .env for development."
    )
    st.markdown(
        """
**How to add secrets (example):**
