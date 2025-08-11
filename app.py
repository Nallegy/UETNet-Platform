import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import requests
import json

# Import the numerology engine we just created
import numerology_engine as ne

# Page configuration
st.set_page_config(
    page_title="Gaia-Net Strategic Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2a5298;
    }
    .sidebar .sidebar-content {
        background: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🌍 Gaia-Net Strategic Intelligence Platform</h1>
    <p>Real-Time Civilizational Monitoring & Sovereignty Analytics</p>
    <p><em>"Light Up the Dark. Build the New."</em></p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🔱 Navigation")
page = st.sidebar.selectbox("Select Intelligence Module", [
    "🏠 Command Center",
    "🔮 Numerology Engine", # <-- NEW PAGE ADDED
    "📊 Regional Sovereignty Index",
    "🌊 Schumann Resonance Monitor",
    "🌾 Food Security Intel",
    "💰 Investment Opportunities",
    "🗺️ Civilizational Risk Map"
])

# --- PAGE ROUTING ---

# Command Center Dashboard
if page == "🏠 Command Center":
    st.header("Command Center - Global Situation Room")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🚨 Global Risk Level</h3>
            <h2 style="color: #e74c3c;">ELEVATED</h2>
            <p>Multiple theaters active</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Opportunity Index</h3>
            <h2 style="color: #27ae60;">HIGH</h2>
            <p>Infrastructure gaps = investment potential</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>⚡ Schumann Frequency</h3>
            <h2 style="color: #3498db;">7.83 Hz</h2>
            <p>Earth's baseline resonance</p>
        </div>
        """, unsafe_allow_html=True)
    st.subheader("🔍 Latest Intelligence Updates")
    updates = [
        {"date": "2025-08-09", "priority": "HIGH", "region": "North America",
         "update": "Inland corridor development accelerating - $200B infrastructure bill passed"},
        {"date": "2025-08-08", "priority": "MEDIUM", "region": "Europe",
         "update": "Netherlands agricultural DAO pilot shows 25% productivity increase"},
    ]
    for update in updates:
        priority_color = {"HIGH": "#e74c3c", "MEDIUM": "#f39c12", "LOW": "#27ae60"}[update["priority"]]
        st.markdown(f"**{update['date']}** | **{update['region']}** | <span style='color: {priority_color}; font-weight: bold;'>{update['priority']}</span> {update['update']}", unsafe_allow_html=True)

# Numerology Engine Page
elif page == "🔮 Numerology Engine":
    st.header("🔮 Resonant Numerology Engine")
    st.markdown("---")
    
    st.subheader("Text-to-Vector Calculator")
    user_input = st.text_area("Enter text, phrase, or name to calculate its numerological vector:", "In the beginning ΑΩ")
    
    if user_input:
        # Calculate the vector using the imported engine
        vector_result = ne.numerology_vector(user_input)
        st.json(vector_result)

    st.markdown("---")
    st.subheader("Glyph & Rune Registry")
    st.write("A foundational registry of characters with known symbolic and energetic properties.")
    
    # Display the glyph registry as a dataframe
    df_glyphs = pd.DataFrame(ne.glyph_registry)
    st.dataframe(df_glyphs, use_container_width=True)


# Regional Sovereignty Index
elif page == "📊 Regional Sovereignty Index":
    st.header("Regional Sovereignty Index (RSI)")
    # ... (rest of the page code is unchanged)
    st.subheader("Civilizational Resilience Metrics by Region")
    regions_data = {
        'Region': ['North America', 'Europe', 'Middle East', 'Asia-Pacific', 'Latin America', 'Africa'],
        'Resource Sovereignty': [85, 45, 90, 70, 85, 90],
        'Infrastructure Sovereignty': [75, 65, 75, 85, 35, 25],
        'Cultural Sovereignty': [70, 65, 45, 40, 70, 80],
        'Governance Sovereignty': [60, 55, 45, 30, 25, 35],
        'Overall RSI': [72, 58, 64, 56, 54, 58]
    }
    df = pd.DataFrame(regions_data)
    st.dataframe(df, use_container_width=True)
    fig = go.Figure()
    categories = ['Resource Sovereignty', 'Infrastructure Sovereignty',
                 'Cultural Sovereignty', 'Governance Sovereignty']
    for i, region in enumerate(df['Region']):
        values = [df.iloc[i][cat] for cat in categories]
        values += values[:1]
        fig.add_trace(go.Scatterpolar(r=values, theta=categories + [categories[0]], fill='toself', name=region))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, title="Regional Sovereignty Comparison")
    st.plotly_chart(fig, use_container_width=True)


# ... (The code for all other pages remains the same) ...


# Schumann Resonance Monitor
elif page == "🌊 Schumann Resonance Monitor":
    st.header("Schumann Resonance Monitoring")
    st.subheader("Earth's Electromagnetic Heartbeat")
    dates = pd.date_range(start='2025-08-01', end='2025-08-09', freq='H')
    base_freq = 7.83
    variations = np.random.normal(0, 0.5, len(dates))
    frequencies = base_freq + variations
    df_schumann = pd.DataFrame({'datetime': dates, 'frequency': frequencies, 'amplitude': np.random.uniform(10, 50, len(dates))})
    fig = px.line(df_schumann, x='datetime', y='frequency', title='Schumann Resonance Frequency (7-Day Window)')
    fig.add_hline(y=7.83, line_dash="dash", line_color="red", annotation_text="Baseline: 7.83 Hz")
    st.plotly_chart(fig, use_container_width=True)
    current_freq = frequencies[-1]
    st.metric("Current Frequency", f"{current_freq:.2f} Hz", f"{current_freq - base_freq:+.2f} Hz")
    if abs(current_freq - base_freq) > 1.0:
        st.warning("⚠️ Significant deviation from baseline detected")
    else:
        st.success("✅ Frequency within normal parameters")

# Food Security Intel
elif page == "🌾 Food Security Intel":
    st.header("Global Food Security Intelligence")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🚨 Critical Vulnerabilities")
        vulnerabilities = ["85% of US beef processing controlled by 4 companies", "80% nitrogen fertilizer import dependency", "40% reduction in Ukrainian grain exports", "200-300% fertilizer price increases (2022-2024)", "Only 9% of consumer food dollar reaches farmers"]
        for vuln in vulnerabilities:
            st.write(f"• {vuln}")
    with col2:
        st.subheader("💡 Investment Opportunities")
        opportunities = ["Regional Food Hubs: $1-5M, 15-25% ROI", "Small Processing Facilities: $500K-2M, 20-30% ROI", "Direct-to-Consumer Platforms: $100K-1M, 25-40% ROI", "Regenerative Agriculture: $250K-1M, 12-20% ROI", "Food Storage/Preservation: $50K-500K, 18-28% ROI"]
        for opp in opportunities:
            st.write(f"• {opp}")
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    wheat_prices = [280, 295, 315, 330, 310, 298, 305, 320]
    corn_prices = [220, 235, 245, 240, 238, 245, 250, 255]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=wheat_prices, name='Wheat ($/bushel)', line=dict(color='#e74c3c')))
    fig.add_trace(go.Scatter(x=months, y=corn_prices, name='Corn ($/bushel)', line=dict(color='#f39c12')))
    fig.update_layout(title='Staple Commodity Price Tracking (2025)', xaxis_title='Month', yaxis_title='Price ($)')
    st.plotly_chart(fig, use_container_width=True)

# Investment Opportunities
elif page == "💰 Investment Opportunities":
    st.header("Strategic Investment Opportunities")
    st.subheader("Sovereignty-Aligned Capital Deployment")
    investment_data = {'Category': ['Food Sovereignty', 'Energy Independence', 'Communication Networks', 'Manufacturing Sovereignty', 'Regenerative Agriculture', 'Water Security'], 'Market Size ($B)': [250, 500, 150, 800, 100, 75], 'Investment Required ($B)': [25, 200, 15, 400, 50, 30], 'Expected ROI (%)': [22, 18, 35, 25, 16, 20], 'Time to Breakeven (years)': [3, 5, 2, 7, 4, 3]}
    df_investments = pd.DataFrame(investment_data)
    st.dataframe(df_investments, use_container_width=True)
    fig = px.scatter(df_investments, x='Investment Required ($B)', y='Expected ROI (%)', size='Market Size ($B)', color='Category', title='Investment Opportunity Matrix: ROI vs Capital Required')
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("🎯 Priority Investment Targets")
    priority_investments = [{"title": "Midwest Food Hub Network", "size": "$5-15M", "roi": "25-35%", "timeline": "18 months"}, {"title": "Texas Solar Microgrid Cooperative", "size": "$10-25M", "roi": "18-24%", "timeline": "24 months"}, {"title": "Netherlands Agricultural DAO", "size": "$2-8M", "roi": "20-30%", "timeline": "12 months"}, {"title": "Mexico Nearshoring Manufacturing", "size": "$25-100M", "roi": "22-28%", "timeline": "36 months"}]
    for inv in priority_investments:
        with st.expander(f"📈 {inv['title']} - {inv['size']} - {inv['roi']} ROI"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Investment Size", inv['size'])
            with col2:
                st.metric("Expected ROI", inv['roi'])
            with col3:
                st.metric("Timeline", inv['timeline'])

# Civilizational Risk Map
elif page == "🗺️ Civilizational Risk Map":
    st.header("Global Risk Assessment Matrix")
    risk_data = {'Risk Category': ['Kinetic Disruption', 'Information Warfare', 'Economic Warfare', 'Regulatory Warfare', 'Biological Warfare', 'Supply Chain Disruption'], 'Probability (%)': [30, 80, 90, 95, 40, 70], 'Impact Severity (1-10)': [8, 9, 9, 8, 10, 7], 'Mitigation Cost ($B)': [100, 50, 200, 25, 150, 75], 'Time Horizon (years)': [5, 1, 2, 3, 8, 2]}
    df_risks = pd.DataFrame(risk_data)
    fig = px.scatter(df_risks, x='Probability (%)', y='Impact Severity (1-10)', size='Mitigation Cost ($B)', color='Risk Category', title='Civilizational Threat Assessment Matrix')
    fig.add_hline(y=7.5, line_dash="dash", line_color="red", opacity=0.5)
    fig.add_vline(x=50, line_dash="dash", line_color="red", opacity=0.5)
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("🎯 Priority Risk Mitigation")
    high_priority = df_risks[(df_risks['Probability (%)'] > 50) & (df_risks['Impact Severity (1-10)'] > 7)]
    for _, risk in high_priority.iterrows():
        st.warning(f"**{risk['Risk Category']}:** {risk['Probability (%)']}% probability, Impact: {risk['Impact Severity (1-10)']}/10, Mitigation: ${risk['Mitigation Cost ($B)']}B required")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d;">
    <p><strong>Sol Innovations Strategic Intelligence</strong> | <em>Prepared by John Michael Narvaez</em></p>
    <p>📧 Solinno@proton.me | 🐦 @AnthoAnalyst</p>
    <p>🔱 <em>For the Sovereignty Architects and Civilization Builders</em></p>
</div>
""", unsafe_allow_html=True)
