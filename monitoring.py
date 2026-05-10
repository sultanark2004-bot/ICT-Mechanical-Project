import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_analytics_page(data):
    """Render the Deep Dive Analytics page"""
    
    st.title("📊 Advanced Engineering Analytics")
    st.markdown("---")

    # --- Section 1: Statistical Distribution ---
    st.subheader("🎯 Sensor Distribution & Variance")
    st.info("Analyze how sensor readings are distributed to identify mechanical drift or outliers.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature Distribution with Box Plot
        fig_dist = px.histogram(
            data, x="temperature", 
            nbins=30, 
            title="Temperature Variance Analysis",
            color_discrete_sequence=['#ef4444'],
            marginal="box" 
        )
        fig_dist.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_dist, use_container_width=True)

    with col2:
        # Vibration vs RPM Scatter - Key for Mechanical Wear Analysis
        fig_scatter = px.scatter(
            data, x="rpm", y="vibration",
            trendline="ols", # Requires: pip install statsmodels
            title="RPM vs. Vibration Correlation",
            color_discrete_sequence=['#f59e0b'],
            hover_data=['timestamp']
        )
        fig_scatter.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # --- Section 2: Correlation Heatmap ---
    st.subheader("🔗 System Interdependency")
    
    # Selecting only numeric columns for correlation
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    corr = data[numeric_cols].corr()
    
    fig_corr = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title="Sensor Relationship Matrix (Pearson Correlation)"
    )
    fig_corr.update_layout(height=500)
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.caption("A value of 1.0 indicates a perfect positive relationship, while -1.0 indicates an inverse relationship.")

    st.markdown("---")

    # --- Section 3: Performance Stability Benchmarks ---
    st.subheader("📈 Stability Benchmarks")
    
    c1, c2, c3 = st.columns(3)
    
    # Logic: Stability = 100 - (Standard Deviation / Mean * 100)
    def calc_stability(series):
        cv = series.std() / series.mean()
        return max(0, 100 - (cv * 100))

    with c1:
        temp_stability = calc_stability(data['temperature'])
        st.metric("Thermal Stability", f"{temp_stability:.1f}%", f"{data['temperature'].std():.2f} σ")
        st.progress(temp_stability / 100)
        
    with c2:
        pressure_stability = calc_stability(data['pressure'])
        st.metric("Pressure Stability", f"{pressure_stability:.1f}%", f"{data['pressure'].std():.2f} σ")
        st.progress(pressure_stability / 100)
        
    with c3:
        vibration_stability = calc_stability(data['vibration'])
        st.metric("Mechanical Balance", f"{vibration_stability:.1f}%", f"{data['vibration'].std():.2f} σ")
        st.progress(vibration_stability / 100)

    # --- Section 4: Data Explorer ---
    with st.expander("🔍 View Raw Statistical Descriptive"):
        st.write("Aggregated summary statistics for all active sensors:")
        st.dataframe(data.describe(), use_container_width=True)
