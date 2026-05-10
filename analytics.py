"""
ICT Mechanical Engineering Dashboard
A professional-grade engineering monitoring and analytics platform
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="ICT Mechanical Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
def load_custom_css():
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Main container */
        .main {
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
        }
        
        /* Metric cards */
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 1rem;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Header gradient */
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: white;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
        }
        
        /* Card container */
        .card {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
        }
        
        /* Status indicators */
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online {
            background-color: #10b981;
            box-shadow: 0 0 10px #10b981;
        }
        
        .status-warning {
            background-color: #f59e0b;
            box-shadow: 0 0 10px #f59e0b;
        }
        
        .status-offline {
            background-color: #ef4444;
            box-shadow: 0 0 10px #ef4444;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Metric value styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    if 'user_activity' not in st.session_state:
        st.session_state.user_activity = []
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []

# Load data with caching
@st.cache_data
def load_sample_data():
    """Generate sample sensor and monitoring data"""
    dates = pd.date_range(end=datetime.now(), periods=100, freq='H')
    
    data = pd.DataFrame({
        'timestamp': dates,
        'temperature': np.random.normal(75, 5, 100),
        'pressure': np.random.normal(100, 10, 100),
        'rpm': np.random.normal(1500, 100, 100),
        'vibration': np.random.normal(0.5, 0.1, 100),
        'network_throughput': np.random.normal(85, 10, 100),
        'cpu_usage': np.random.normal(60, 15, 100),
        'memory_usage': np.random.normal(70, 10, 100),
        'system_uptime': np.random.uniform(95, 100, 100)
    })
    
    return data

# Create header
def render_header():
    st.markdown("""
        <div class="header-container">
            <h1 style="margin: 0; font-size: 2.5rem;">⚙️ ICT Mechanical Engineering Dashboard</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">
                Advanced Monitoring & Analytics Platform
            </p>
        </div>
    """, unsafe_allow_html=True)

# Create KPI metrics
def render_kpi_metrics(data):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🌡️ Avg Temperature",
            value=f"{data['temperature'].mean():.1f}°F",
            delta=f"{data['temperature'].iloc[-1] - data['temperature'].mean():.1f}°F"
        )
    
    with col2:
        st.metric(
            label="⚡ System Uptime",
            value=f"{data['system_uptime'].mean():.2f}%",
            delta=f"{data['system_uptime'].iloc[-1] - data['system_uptime'].mean():.2f}%"
        )
    
    with col3:
        st.metric(
            label="🔄 Avg RPM",
            value=f"{data['rpm'].mean():.0f}",
            delta=f"{data['rpm'].iloc[-1] - data['rpm'].mean():.0f}"
        )
    
    with col4:
        st.metric(
            label="📊 Network Efficiency",
            value=f"{data['network_throughput'].mean():.1f}%",
            delta=f"{data['network_throughput'].iloc[-1] - data['network_throughput'].mean():.1f}%"
        )

# Create system status cards
def render_status_cards():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card">
                <h3>🟢 Mechanical Systems</h3>
                <p><span class="status-indicator status-online"></span>All systems operational</p>
                <p style="color: #6b7280; margin-top: 1rem;">Last check: 2 minutes ago</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card">
                <h3>🟡 ICT Infrastructure</h3>
                <p><span class="status-indicator status-warning"></span>Minor alerts detected</p>
                <p style="color: #6b7280; margin-top: 1rem;">Last check: 1 minute ago</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card">
                <h3>🟢 Data Analytics</h3>
                <p><span class="status-indicator status-online"></span>Processing normally</p>
                <p style="color: #6b7280; margin-top: 1rem;">Last check: 30 seconds ago</p>
            </div>
        """, unsafe_allow_html=True)

# Create real-time monitoring charts
def render_monitoring_charts(data):
    st.subheader("📈 Real-Time Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature trend
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=data['timestamp'],
            y=data['temperature'],
            mode='lines',
            name='Temperature',
            line=dict(color='#ef4444', width=2),
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.1)'
        ))
        fig_temp.update_layout(
            title='Temperature Monitoring',
            xaxis_title='Time',
            yaxis_title='Temperature (°F)',
            hovermode='x unified',
            template='plotly_white',
            height=300
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # RPM monitoring
        fig_rpm = go.Figure()
        fig_rpm.add_trace(go.Scatter(
            x=data['timestamp'],
            y=data['rpm'],
            mode='lines',
            name='RPM',
            line=dict(color='#3b82f6', width=2),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.1)'
        ))
        fig_rpm.update_layout(
            title='RPM Monitoring',
            xaxis_title='Time',
            yaxis_title='RPM',
            hovermode='x unified',
            template='plotly_white',
            height=300
        )
        st.plotly_chart(fig_rpm, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Pressure monitoring
        fig_pressure = go.Figure()
        fig_pressure.add_trace(go.Scatter(
            x=data['timestamp'],
            y=data['pressure'],
            mode='lines',
            name='Pressure',
            line=dict(color='#10b981', width=2),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ))
        fig_pressure.update_layout(
            title='Pressure Monitoring',
            xaxis_title='Time',
            yaxis_title='Pressure (PSI)',
            hovermode='x unified',
            template='plotly_white',
            height=300
        )
        st.plotly_chart(fig_pressure, use_container_width=True)
    
    with col4:
        # Network throughput
        fig_network = go.Figure()
        fig_network.add_trace(go.Scatter(
            x=data['timestamp'],
            y=data['network_throughput'],
            mode='lines',
            name='Network Throughput',
            line=dict(color='#8b5cf6', width=2),
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.1)'
        ))
        fig_network.update_layout(
            title='Network Throughput',
            xaxis_title='Time',
            yaxis_title='Throughput (%)',
            hovermode='x unified',
            template='plotly_white',
            height=300
        )
        st.plotly_chart(fig_network, use_container_width=True)

# Sidebar
def render_sidebar():
    with st.sidebar:
        st.markdown("### 🎛️ Navigation")
        
        page = st.radio(
            "Select Page",
            ["🏠 Home Dashboard", "📊 Analytics", "📋 Reports", "🔧 Monitoring", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        st.markdown("### 📅 Date Range")
        date_range = st.date_input(
            "Select range",
            value=(datetime.now() - timedelta(days=7), datetime.now()),
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        st.markdown("### 🔔 System Alerts")
        st.info("✅ All systems operational")
        st.warning("⚠️ Scheduled maintenance: May 15")
        
        st.markdown("---")
        
        st.markdown("### 📈 Quick Stats")
        st.metric("Active Sensors", "47", "+3")
        st.metric("Data Points Today", "12.4K", "+8%")
        
        return page

# Main application
def main():
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Render header
    render_header()
    
    # Load data
    data = load_sample_data()
    
    # Route to appropriate page
    if page == "🏠 Home Dashboard":
        render_kpi_metrics(data)
        st.markdown("<br>", unsafe_allow_html=True)
        render_status_cards()
        st.markdown("<br>", unsafe_allow_html=True)
        render_monitoring_charts(data)
        
    elif page == "📊 Analytics":
        from pages.analytics import render_analytics_page
        render_analytics_page(data)
        
    elif page == "📋 Reports":
        from pages.reports import render_reports_page
        render_reports_page(data)
        
    elif page == "🔧 Monitoring":
        from pages.monitoring import render_monitoring_page
        render_monitoring_page(data)
        
    elif page == "⚙️ Settings":
        from pages.settings import render_settings_page
        render_settings_page()

if __name__ == "__main__":
    main()
