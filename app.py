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
import yfinance as yf

# --- Resonant Configuration ---
class Config:
    """Holds all static configuration for the Gaia-Net platform."""
    CACHE_TTL_REALTIME = 300
    CACHE_TTL_DYNAMIC = 900
    CACHE_TTL_STATIC = 3600
    USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    NOAA_SOLAR_FLUX_URL = "https://services.swpc.noaa.gov/json/f107_dly.json"
    INTEL_FALLBACK_URL = "https://raw.githubusercontent.com/NALLEGY/UETNet-Platform/main/intel_updates.json"
    GW5_FALLBACK_URL = "https://raw.githubusercontent.com/NALLEGY/UETNet-Platform/main/5gw_data.json"
    MAIN_GRADIENT = "linear-gradient(135deg, rgba(6,14,46,1) 0%, rgba(11,22,64,1) 35%, rgba(18,35,87,1) 100%)"
    BASE_RESONANT_COLORS = ['#00bfff', '#ffd700', '#ff4500', '#adff2f', '#da70d6', '#ffffff']

# --- Module Availability Check ---
try:
    import numerology_engine as ne
    NUMEROLOGY_AVAILABLE = True
except ImportError:
    NUMEROLOGY_AVAILABLE = False
    class DummyNumerologyEngine:
        def numerology_vector(self, text: str) -> Dict[str, Any]: return {"error": "Engine not found", "pyth": 0}
    ne = DummyNumerologyEngine()

# --- Data Ingestion Layer ---
@st.cache_data(ttl=Config.CACHE_TTL_DYNAMIC)
def load_json_data(local_path: str, remote_url: str) -> Any:
    """Loads a JSON file from a local path with a remote fallback."""
    try:
        with open(local_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        try:
            r = requests.get(remote_url, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            st.error(f"Failed to load {local_path} from remote: {e}")
            return None
    except Exception as e:
        st.error(f"Error loading {local_path}: {e}")
        return None

@st.cache_data(ttl=Config.CACHE_TTL_REALTIME)
def get_live_seismic_data(days: int = 30, min_magnitude: float = 4.5) -> pd.DataFrame:
    """Fetches live seismic data from the USGS API."""
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        params = {"format": "geojson", "starttime": start_time.strftime("%Y-%m-%d"), "endtime": end_time.strftime("%Y-%m-%d"), "minmagnitude": min_magnitude}
        response = requests.get(Config.USGS_API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        records = [{'date': pd.to_datetime(f['properties']['time'], unit='ms'), 'lat': f['geometry']['coordinates'][1], 'lon': f['geometry']['coordinates'][0], 'magnitude': f['properties']['mag'], 'place': f['properties']['place']} for f in data.get('features', [])]
        return pd.DataFrame(records) if records else pd.DataFrame(columns=['date', 'lat', 'lon', 'magnitude', 'place'])
    except requests.exceptions.RequestException as e:
        st.error(f"Network error fetching seismic data: {e}")
        return pd.DataFrame(columns=['date', 'lat', 'lon', 'magnitude', 'place'])

@st.cache_data(ttl=Config.CACHE_TTL_STATIC)
def get_live_solar_data() -> pd.DataFrame:
    """Fetches live F10.7cm solar flux data from NOAA."""
    try:
        response = requests.get(Config.NOAA_SOLAR_FLUX_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        df['time_tag'] = pd.to_datetime(df['time_tag'])
        df = df.rename(columns={'time_tag': 'date', 'flux': 'solar_flux'})
        return df[['date', 'solar_flux']]
    except Exception as e:
        st.error(f"Failed to fetch live solar data: {e}")
        return pd.DataFrame(columns=['date', 'solar_flux'])

@st.cache_data(ttl=Config.CACHE_TTL_REALTIME)
def get_live_vix_data(days: int = 365) -> pd.DataFrame:
    """Fetches live VIX data using yfinance."""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        vix = yf.Ticker("^VIX")
        hist = vix.history(start=start_date, end=end_date)
        df = pd.DataFrame(hist['Close']).rename(columns={'Close': 'vix'})
        df.index.name = 'date'
        return df.reset_index()
    except Exception as e:
        st.error(f"Failed to fetch VIX data: {e}")
        return pd.DataFrame(columns=['date', 'vix'])

@st.cache_data(ttl=Config.CACHE_TTL_STATIC)
def get_schumann_data(days: int = 1) -> Tuple[Optional[pd.DataFrame], Optional[datetime]]:
    """Generate placeholder Schumann resonance data."""
    try:
        end_time = datetime.now(); start_time = end_time - timedelta(days=days); dates = pd.date_range(start=start_time, end=end_time, freq='h'); base_freq = 7.83; noise = np.random.normal(0, 0.1, len(dates)); spikes = np.zeros(len(dates)); num_spikes = int(days * np.random.uniform(3, 6));
        if num_spikes > 0:
            spike_indices = np.random.choice(len(dates), size=min(num_spikes, len(dates)), replace=False); spike_magnitudes = np.random.uniform(1, 3, size=len(spike_indices)); spikes[spike_indices] = spike_magnitudes
        frequencies = base_freq + noise + spikes; df = pd.DataFrame({'datetime': dates, 'frequency': frequencies})
        return df, datetime.now()
    except Exception as e:
        st.error(f"Error generating Schumann data: {e}"); return pd.DataFrame(columns=['datetime', 'frequency']), None

# --- Visualization & Theming Layer (Unchanged) ---
def get_numerology_color_sequence(date_str: str) -> List[str]:
    value = sum(int(c) for c in date_str if c.isdigit()) % len(Config.BASE_RESONANT_COLORS)
    return Config.BASE_RESONANT_COLORS[value:] + Config.BASE_RESONANT_COLORS[:value]
def apply_resonant_theming():
    st.markdown(f"""<style>...</style>""", unsafe_allow_html=True) # CSS is unchanged
    resonant_colors = get_numerology_color_sequence(datetime.now().strftime("%Y%m%d"))
    px.defaults.template = "plotly_dark"; px.defaults.color_discrete_sequence = resonant_colors
    return resonant_colors
def inject_sidecar_metadata(page_name: str, content_text: str):
    sidecar = {"page": page_name, "generated_utc": datetime.utcnow().isoformat()+"Z", "numerology": ne.numerology_vector(content_text), "geometry": {"template":"golden-618-382","phi":1.618}}
    st.components.v1.html(f"<script id='uet-sidecar' type='application/json'>{json.dumps(sidecar)}</script>", height=0)

# --- UI & Page Layout Layer ---
def render_command_center():
    st.header("Command Center: Global Situation Room")
    col1, col2, col3 = st.columns([1.618, 1.618, 1.618])
    with col1: st.markdown("""<div class="metric-card"><h3>🚨 Global Risk</h3><h2 style="color: #ff4500;">ELEVATED</h2><p>Multiple theaters active</p></div>""", unsafe_allow_html=True)
    with col2: st.markdown("""<div class="metric-card"><h3>🎯 Opportunity</h3><h2 style="color: #adff2f;">HIGH</h2><p>Infrastructure gaps</p></div>""", unsafe_allow_html=True)
    with col3: st.markdown("""<div class="metric-card"><h3>⚡ Resonance</h3><h2 style="color: #00bfff;">7.83 Hz</h2><p>Earth's baseline</p></div>""", unsafe_allow_html=True)
    st.markdown("---"); st.subheader("🔍 Latest Intelligence Updates")
    updates = load_json_data('intel_updates.json', Config.INTEL_FALLBACK_URL)
    if updates:
        for update in updates:
            priority_color = {"CRITICAL": "#ff4500", "HIGH": "#ffd700", "MEDIUM": "#00bfff", "LOW": "#adff2f"}.get(update.get("priority"), "#e0e0e0")
            st.markdown(f"**{update.get('date')}** | **{update.get('region')}** | <span style='color: {priority_color}; font-weight: bold;'>{update.get('priority')}</span>: {update.get('update')}", unsafe_allow_html=True)

def render_cyclical_convergence():
    st.header("🌀 Cyclical Convergence Monitor")
    st.info("Visualizing the convergence of Solar, Seismic, and Societal cycles.")
    days_to_view = st.slider("Select Timeframe (Days)", 30, 365*3, 365, 30, key="cc_slider")
    
    with st.spinner("Fetching live cyclical data..."):
        df_solar = get_live_solar_data()
        df_vix = get_live_vix_data(days=days_to_view)
        df_seismic = get_live_seismic_data(days=days_to_view, min_magnitude=4.5)

    st.subheader("Live Solar Flux & Market Volatility")
    if not df_solar.empty and not df_vix.empty:
        fig_cycles = go.Figure(); fig_cycles.add_trace(go.Scatter(x=df_solar['date'], y=df_solar['solar_flux'], name='Solar Flux (F10.7cm)', yaxis='y1')); fig_cycles.add_trace(go.Scatter(x=df_vix['date'], y=df_vix['vix'], name='Market Volatility (VIX)', yaxis='y2')); fig_cycles.update_layout(yaxis=dict(title="Solar Flux"), yaxis2=dict(title="VIX Index", overlaying='y', side='right')); st.plotly_chart(fig_cycles, use_container_width=True)
    else:
        st.warning("Could not display Solar/VIX chart. One or more data sources are unavailable.")
    
    st.subheader("Live Global Seismic Activity (from USGS)")
    if not df_seismic.empty:
        fig_seismic = px.scatter_geo(df_seismic, lat='lat', lon='lon', size='magnitude', hover_name='place', projection="natural earth", title=f"Major Earthquakes (M4.5+) in last {days_to_view} days", color="magnitude", color_continuous_scale=px.colors.sequential.OrRd)
        st.plotly_chart(fig_seismic, use_container_width=True)
    else:
        st.warning("No significant seismic events recorded in the selected timeframe.")

def render_5gw_dashboard():
    st.header("🛡️ 5th-Generation Warfare Dashboard")
    st.info("Tracking the non-kinetic battlefields of narrative, regulation, and information.")
    data = load_json_data('5gw_data.json', Config.GW5_FALLBACK_URL)
    if data:
        df_narratives = pd.DataFrame(data['narratives'])
        df_regulatory = pd.DataFrame(data['regulatory'])
        
        st.subheader("Narrative Momentum Tracker")
        fig_narratives = px.line(df_narratives, x='date', y=df_narratives.columns[1:], title="Frequency of Key Narratives Over Time")
        st.plotly_chart(fig_narratives, use_container_width=True)
        
        st.subheader("Regulatory Warfare Map")
        fig_reg = go.Figure(data=go.Choropleth(locations=df_regulatory['country_iso'], z=df_regulatory['Digital ID Status'].astype(float), colorscale='Blues', colorbar_title="Digital ID Status", text=df_regulatory['country_iso']))
        fig_reg.update_layout(title_text='Global Digital ID Implementation Status', geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'))
        st.plotly_chart(fig_reg, use_container_width=True)

def render_placeholder_page(title: str, image_text: str):
    st.header(f"{title}"); st.info("This module is under construction."); st.image(f"https://placehold.co/1200x500/0d1b3e/ffffff?text={image_text.replace(' ', '+')}", use_column_width=True)

def render_numerology_engine():
    st.header("🔮 Resonant Numerology Engine")
    if not NUMEROLOGY_AVAILABLE:
        st.error("Numerology Engine module could not be loaded."); return
    st.markdown("---"); st.subheader("Text-to-Vector Calculator"); user_input = st.text_area("Enter text:", "In the beginning ΑΩ", label_visibility="collapsed")
    if user_input: st.json(ne.numerology_vector(user_input))
    st.markdown("---"); st.subheader("Glyph & Rune Registry"); st.dataframe(pd.DataFrame(ne.glyph_registry), use_container_width=True)

# --- Main Application Logic ---
def main():
    st.set_page_config(page_title="Gaia-Net Strategic Intelligence", page_icon="⚜️", layout="wide")
    if not NUMEROLOGY_AVAILABLE:
        st.warning("Numerology engine module (`numerology_engine.py`) not found.")
    apply_resonant_theming()
    st.markdown("""<div class="main-header"><h1>⚜️ Gaia-Net Strategic Intelligence</h1><p><em>"Light Up the Dark. Build the New."</em></p></div>""", unsafe_allow_html=True)
    inject_sidecar_metadata("main_view", "Gaia-Net Strategic Intelligence")
    st.sidebar.title("🔱 Navigation Core")
    page = st.sidebar.selectbox("Select Intelligence Module", ["🏠 Command Center", "🌀 Cyclical Convergence", "🛡️ 5th-Gen Warfare", "🔑 Hidden Patterns", "🌐 Geo-Esoteric Map", "⏳ Resonance Timeline", "⚜️ Sacred Patterns", "🔮 Numerology Engine", "🌊 Schumann Monitor", "📊 Sovereignty Index"])
    
    page_functions = {
        "🏠 Command Center": render_command_center,
        "🌀 Cyclical Convergence": render_cyclical_convergence,
        "🛡️ 5th-Gen Warfare": render_5gw_dashboard,
        "🔮 Numerology Engine": render_numerology_engine,
    }
    
    if page in page_functions:
        page_functions[page]()
    else:
        render_placeholder_page(page, f"{page.split(' ')[-1]} Module")

    try:
        nvec = ne.numerology_vector("For the Sovereignty Architects and Civilization Builders")
        footer_num_val = nvec.get('pyth') or nvec.get('pythagorean_sum') or "N/A"
    except Exception: footer_num_val = "Error"
    # ... (Footer markdown is unchanged) ...

if __name__ == "__main__":
    main()
