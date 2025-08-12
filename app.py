import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import requests
import json
import base64
import hashlib
from typing import Tuple, Dict, Any, List, Optional

# --- Resonant Configuration ---
# Defining the core energetic and structural constants of the platform.

class Config:
    """Holds all static configuration for the Gaia-Net platform."""
    # Caching TTLs (Time-To-Live) in seconds
    CACHE_TTL_REALTIME = 300    # 5 minutes for live data like seismic
    CACHE_TTL_DYNAMIC = 900     # 15 minutes for semi-static data like intel updates
    CACHE_TTL_STATIC = 3600     # 1 hour for placeholders or stable data

    # API and Data Source URLs
    USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    # IMPORTANT: Replace with your actual raw GitHub file URL for intel_updates.json
    INTEL_FALLBACK_URL = "https://raw.githubusercontent.com/NALLEGY/UETNet-Platform/main/intel_updates.json"

    # Theming & Resonance
    MAIN_GRADIENT = "linear-gradient(135deg, rgba(6,14,46,1) 0%, rgba(11,22,64,1) 35%, rgba(18,35,87,1) 100%)"
    BASE_RESONANT_COLORS = ['#00bfff', '#ffd700', '#ff4500', '#adff2f', '#da70d6', '#ffffff']

# --- Module Availability Check ---
# Ensures the platform can run gracefully even if optional modules are missing.
try:
    import numerology_engine as ne
    NUMEROLOGY_AVAILABLE = True
except ImportError:
    NUMEROLOGY_AVAILABLE = False
    # Define a dummy function to prevent crashes if the engine is missing
    class DummyNumerologyEngine:
        def numerology_vector(self, text: str) -> Dict[str, Any]:
            return {"error": "Engine not found", "pyth": 0}
    ne = DummyNumerologyEngine()

# --- Data Ingestion Layer ---
# Hardened functions for fetching data from external and internal sources.

@st.cache_data(ttl=Config.CACHE_TTL_DYNAMIC)
def load_intel_updates() -> List[Dict[str, Any]]:
    """Loads intelligence updates from a local JSON file with a remote fallback."""
    try:
        with open('intel_updates.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        try:
            r = requests.get(Config.INTEL_FALLBACK_URL, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return [{"date": "Error", "priority": "CRITICAL", "region": "System", "update": f"Failed to load intel_updates.json from remote: {e}"}]
    except Exception as e:
        return [{"date": "Error", "priority": "CRITICAL", "region": "System", "update": f"Error loading intel_updates.json: {e}"}]

@st.cache_data(ttl=Config.CACHE_TTL_REALTIME)
def get_live_seismic_data(days: int = 30, min_magnitude: float = 4.5) -> pd.DataFrame:
    """Fetches live seismic data from the USGS API with robust error handling."""
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        params = {
            "format": "geojson",
            "starttime": start_time.strftime("%Y-%m-%d"),
            "endtime": end_time.strftime("%Y-%m-%d"),
            "minmagnitude": min_magnitude
        }
        response = requests.get(Config.USGS_API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        records = [
            {
                'date': pd.to_datetime(f['properties']['time'], unit='ms'),
                'lat': f['geometry']['coordinates'][1],
                'lon': f['geometry']['coordinates'][0],
                'magnitude': f['properties']['mag'],
                'place': f['properties']['place']
            }
            for f in data.get('features', [])
        ]
        return pd.DataFrame(records) if records else pd.DataFrame(columns=['date', 'lat', 'lon', 'magnitude', 'place'])
    except requests.exceptions.RequestException as e:
        st.error(f"Network error fetching seismic data: {e}")
        return pd.DataFrame(columns=['date', 'lat', 'lon', 'magnitude', 'place'])

@st.cache_data(ttl=Config.CACHE_TTL_STATIC)
def get_placeholder_cyclical_data(days: int = 365) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate placeholder solar and VIX data for testing."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq='D')
    
    # Solar cycle simulation (11-year cycle)
    solar_cycle_length = 365 * 11
    days_since_ref = (dates - datetime(2019, 12, 1)).days
    solar_phase = days_since_ref / solar_cycle_length * 2 * np.pi
    sunspots = 50 * (1 - np.cos(solar_phase)) + np.random.normal(0, 5, len(dates)) + 10
    df_solar = pd.DataFrame({'date': dates, 'sunspots': sunspots.clip(0)})
        
    # VIX simulation with occasional spikes
    vix = 15 + np.random.normal(0, 2, len(dates))
    for _ in range(int(days / 90)):
        spike_idx = np.random.randint(0, len(dates))
        vix[spike_idx:spike_idx+3] += np.random.uniform(10, 30)
    df_vix = pd.DataFrame({'date': dates, 'vix': vix.clip(10)})
        
    return df_solar, df_vix

# ... (Other placeholder functions remain for now, but are more readable) ...

# --- Visualization & Theming Layer ---
# Functions that define the resonant aesthetic of the platform.

def get_numerology_color_sequence(date_str: str) -> List[str]:
    """Generates a cosmically 'tuned' color sequence for the day."""
    value = sum(int(c) for c in date_str if c.isdigit()) % len(Config.BASE_RESONANT_COLORS)
    return Config.BASE_RESONANT_COLORS[value:] + Config.BASE_RESONANT_COLORS[:value]

def apply_resonant_theming():
    """Applies the main CSS and sets the daily color theme."""
    st.markdown(f"""<style>...</style>""", unsafe_allow_html=True) # CSS remains the same as previous version
    resonant_colors = get_numerology_color_sequence(datetime.now().strftime("%Y%m%d"))
    px.defaults.template = "plotly_dark"
    px.defaults.color_discrete_sequence = resonant_colors
    return resonant_colors

def inject_sidecar_metadata(page_name: str, content_text: str):
    """Embeds hidden UET metadata into the page's HTML for encoding."""
    sidecar = {
      "page": page_name,
      "generated_utc": datetime.utcnow().isoformat()+"Z",
      "numerology": ne.numerology_vector(content_text),
      "geometry": {"template":"golden-618-382","phi":1.618}
    }
    st.components.v1.html(f"<script id='uet-sidecar' type='application/json'>{json.dumps(sidecar)}</script>", height=0)

# --- UI & Page Layout Layer ---
# Functions that define the structure and content of each dashboard page.

def render_command_center():
    st.header("Command Center: Global Situation Room")
    # ... (UI code remains the same) ...

def render_cyclical_convergence():
    st.header("🌀 Cyclical Convergence Monitor")
    # ... (UI code remains the same, but now uses the hardened data function) ...
    df_seismic = get_live_seismic_data(days=days_to_view)


# ... (Define a render function for each page for clarity and separation) ...

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(page_title="Gaia-Net Strategic Intelligence", page_icon="⚜️", layout="wide")
    
    if not NUMEROLOGY_AVAILABLE:
        st.warning("Numerology engine module (`numerology_engine.py`) not found. Some features will be disabled.")

    resonant_colors = apply_resonant_theming()
    
    st.markdown("""<div class="main-header"><h1>⚜️ Gaia-Net Strategic Intelligence</h1><p><em>"Light Up the Dark. Build the New."</em></p></div>""")
    inject_sidecar_metadata("main_view", "Gaia-Net Strategic Intelligence")

    st.sidebar.title("🔱 Navigation Core")
    page = st.sidebar.selectbox("Select Intelligence Module", [
        "🏠 Command Center", "🌀 Cyclical Convergence", "🛡️ 5th-Gen Warfare", 
        "🔑 Hidden Patterns", "🌐 Geo-Esoteric Map", "⏳ Resonance Timeline", 
        "⚜️ Sacred Patterns", "🔮 Numerology Engine", "🌊 Schumann Monitor", "📊 Sovereignty Index"
    ])

    # Page routing using a dictionary for clarity
    page_functions = {
        "🏠 Command Center": render_command_center,
        "🌀 Cyclical Convergence": render_cyclical_convergence,
        # ... (map other page names to their render functions) ...
    }
    
    # Execute the render function for the selected page
    if page in page_functions:
        page_functions[page]()
    else:
        # Fallback for pages not yet refactored into functions
        st.write(f"Welcome to the {page} module.")

    # ... (Footer code with critical numerology fix) ...
    try:
        nvec = ne.numerology_vector("For the Sovereignty Architects and Civilization Builders")
        footer_num_val = nvec.get('pyth') or nvec.get('pythagorean_sum') or "N/A"
    except Exception as e:
        footer_num_val = "Error"
    # ... (Rest of the footer markdown) ...

if __name__ == "__main__":
    main()
