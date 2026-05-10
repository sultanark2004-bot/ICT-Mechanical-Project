import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * { font-family: 'Inter', sans-serif; }
        
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
        }
        
        .card {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
            color: #1a202c;
        }

        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online { background-color: #10b981; box-shadow: 0 0 10px #10b981; }
        .status-warning { background-color: #f59e0b; box-shadow: 0 0 10px #f59e0b; }
        
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    # FIXED: Use 'h' instead of 'H' for frequency to support latest Pandas/Python 3.14
    dates = pd.date_range(end=datetime.now(), periods=100, freq='h')
    
    data = pd.DataFrame({
        'timestamp': dates,
        'temperature': np.random.normal(75, 5, 100),
        'pressure': np.random.normal(100, 10, 100),
        'rpm': np.random.normal(1500, 100, 100),
        'vibration': np.random.normal(0.5, 0.1, 100),
        'network_throughput': np.random.normal(85, 10, 100),
        'system_uptime': np.random.uniform(98, 100, 100)
    })
    return data

def render_header():
    st.markdown("""
        <div class="header-container">
            <h1 style="margin: 0; font-size: 2.5rem; color: white;">⚙️ ICT Mechanical Engineering Dashboard</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem; color: white;">
                Advanced Monitoring & Analytics Platform
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_kpi_metrics(data):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌡️ Avg Temp", f"{data['temperature'].mean():.1f}°F")
    with col2:
        st.metric("⚡ Uptime", f"{data['system_uptime'].mean():.2f}%")
    with col3:
        st.metric("🔄 Avg RPM", f"{data['rpm'].mean():.0f}")
    with col4:
        st.metric("📊 Efficiency", f"{data['network_throughput'].mean():.1f}%")

def render_monitoring_charts(data):
    st.subheader("📈 Real-Time Monitoring")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(x=data['timestamp'], y=data['temperature'], fill='tozeroy', line_color='#ef4444'))
        fig_temp.update_layout(title='Temperature (°F)', height=300, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        fig_rpm = go.Figure()
        fig_rpm.add_trace(go.Scatter(x=data['timestamp'], y=data['rpm'], fill='tozeroy', line_color='#3b82f6'))
        fig_rpm.update_layout(title='RPM History', height=300, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_rpm, use_container_width=True)

def main():
    load_custom_css()
    
    # Sidebar
    with st.sidebar:
        st.title("🎛️ Navigation")
        page = st.radio("Go to", ["🏠 Home Dashboard", "📊 Analytics", "📋 Reports"])
        st.divider()
        st.info("System Status: Online")

    render_header()
    data = load_sample_data()

    if page == "🏠 Home Dashboard":
        render_kpi_metrics(data)
        
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="card"><h3>🟢 Mechanical</h3>All systems operational</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="card"><h3>🟡 ICT</h3>Minor latency detected</div>', unsafe_allow_html=True)
            
        render_monitoring_charts(data)
        
    elif page == "📊 Analytics":
        st.header("Deep Data Analysis")
        st.write("Correlation Heatmap")
        corr = data.drop('timestamp', axis=1).corr()
        st.dataframe(corr.style.background_gradient(cmap='coolwarm'))
        
    elif page == "📋 Reports":
        st.header("Shift Reports")
        st.table(data.tail(10))
        st.download_button("Download Full CSV", data.to_csv(), "report.csv")

if __name__ == "__main__":
    main()
