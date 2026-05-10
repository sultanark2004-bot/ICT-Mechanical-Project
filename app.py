import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
import numpy as np
from datetime import datetime

# Must be the first Streamlit command
st.set_page_config(page_title="Nexus ICT-Mechanical", layout="wide", page_icon="🏗️")

# Professional UI Styling
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    [data-testid="stMetricValue"] { font-size: 24px; font-weight: 700; color: #1e3a8a; }
    .stApp { max-width: 100%; }
    </style>
""", unsafe_allow_html=True)

# Generate / Cache Data
@st.cache_data(ttl=1)
def get_system_data():
    # Simulate high-fidelity engineering data
    rows = 100
    data = pd.DataFrame({
        'timestamp': pd.date_range(datetime.now(), periods=rows, freq='min'),
        'temperature': np.random.normal(75, 5, rows),
        'pressure': np.random.normal(100, 10, rows),
        'vibration': np.random.uniform(0.1, 0.8, rows),
        'rpm': np.random.normal(1500, 50, rows),
        'cpu_usage': np.random.uniform(30, 90, rows),
        'network_throughput': np.random.uniform(100, 1000, rows),
        'memory_usage': np.random.uniform(40, 85, rows),
        'system_uptime': [99.9] * rows
    })
    return data

data = get_system_data()

# Professional Sidebar Navigation
with st.sidebar:
    st.title("🛡️ Nexus Control")
    selected = option_menu(
        menu_title=None,
        options=["Monitoring", "Analytics", "Reports"],
        icons=["speedometer2", "graph-up", "file-text"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#ffffff"},
            "nav-link-selected": {"background-color": "#1e3a8a"},
        }
    )
    st.divider()
    st.caption("System Status: OPERATIONAL")
    st.success("Cloud Sync Active")

# Page Routing
if selected == "Monitoring":
    from pages.monitoring import render_monitoring_page
    render_monitoring_page(data)
elif selected == "Analytics":
    from pages.analytics import render_analytics_page
    render_analytics_page(data)
elif selected == "Reports":
    from pages.reports import render_reports_page
    render_reports_page(data)

style_metric_cards(border_left_color="#1e3a8a")
