import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_analytics_page(data):
    st.markdown("## 📊 Deep Dive Analytics")
    st.markdown("---")

    # Layout for top-level analytics
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Correlation Matrix")
        st.write("Understand the relationship between different mechanical variables.")
        # Calculate correlation for numeric columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        corr = data[numeric_cols].corr()
        
        fig_corr = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale='RdBu_r',
            labels=dict(color="Correlation")
        )
        fig_corr.update_layout(height=450, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_corr, use_container_width=True)

    with col2:
        st.subheader("Sensor Distributions")
        selected_sensor = st.selectbox(
            "Select Sensor for Distribution Analysis",
            options=['temperature', 'pressure', 'rpm', 'vibration']
        )
        
        fig_dist = px.histogram(
            data, 
            x=selected_sensor, 
            nbins=30, 
            marginal="box", # Adds a box plot on top
            color_discrete_sequence=['#764ba2']
        )
        fig_dist.update_layout(
            height=450, 
            template="plotly_white",
            xaxis_title=selected_sensor.capitalize(),
            yaxis_title="Frequency"
        )
        To create a professional analytics suite for your **ICT Mechanical Engineering Dashboard**, the `analytics.py` file should focus on statistical correlation, trend forecasting, and mechanical performance distributions.

Here is a high-performance, visually polished version of `analytics.py`. 

### `pages/analytics.py`

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_analytics_page(data):
    st.markdown("## 📊 Advanced Engineering Analytics")
    st.info("Deep dive into sensor correlations and mechanical performance distributions.")

    # --- Section 1: Statistical Distribution ---
    st.subheader("Distribution Analysis")
    col1, col2 = st.columns(2)

    with col1:
        # Temperature Distribution
        fig_dist = px.histogram(
            data, x="temperature", 
            nbins=30, 
            title="Temperature Variance Distribution",
            color_discrete_sequence=['#ef4444'],
            marginal="box" # Adds a box plot on top
        )
        fig_dist.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_dist, use_container_width=True)

    with col2:
        # RPM vs Vibration Scatter
        fig_scatter = px.scatter(
            data, x="rpm", y="vibration",
            trendline="ols",
            title="RPM vs. Vibration Correlation",
            color_discrete_sequence=['#3b82f6']
        )
        fig_scatter.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # --- Section 2: Correlation Heatmap ---
    st.subheader("System Interdependency Heatmap")
    
    # Calculate correlation matrix for numerical columns
    corr = data.drop(columns=['timestamp']).corr()
    
    fig_corr = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title="Sensor Correlation Matrix (Pearson)"
    )
    fig_corr.update_layout(height=500)
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("---")

    # --- Section 3: Performance Efficiency ---
    st.subheader("Efficiency Metrics")
    
    c1, c2, c3 = st.columns(3)
    
    # Simple calculation for a "Health Score"
    avg_temp = data['temperature'].mean()
    health_score = 100 - (data['vibration'].mean() * 10)
    
    with c1:
        st.write("**Operational Health Score**")
        st.header(f"{health_score:.1f}%")
        st.progress(health_score / 100)
        
    with c2:
        st.write("**Average Pressure Stability**")
        stability = 100 - (data['pressure'].std())
        st.header(f"{stability:.1f}%")
        st.progress(stability / 100)
        
    with c3:
        st.write("**Network Reliability**")
        reliability = data['network_throughput'].mean()
        st.header(f"{reliability:.1f}%")
        st.progress(reliability / 100)

    # --- Section 4: Raw Data Drill-down ---
    with st.expander("🔍 View Raw Statistical Summary"):
        st.dataframe(data.describe(), use_container_width=True)
