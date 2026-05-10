import streamlit as st
import plotly.graph_objects as go

def render_monitoring_page(data):
    st.header("🚀 Real-Time System Health")
    
    # Top Row Metrics
    c1, c2, c3, c4 = st.columns(4)
    curr = data.iloc[-1]
    
    c1.metric("Core Temp", f"{curr['temperature']:.1f}°F", "1.2°F")
    c2.metric("Vibration", f"{curr['vibration']:.2f}g", "-0.02g")
    c3.metric("CPU Load", f"{curr['cpu_usage']:.1f}%", "5%")
    c4.metric("Network", f"{int(curr['network_throughput'])} Mbps", "12 Mbps")

    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Mechanical Stress Analysis")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['timestamp'], y=data['temperature'], name="Thermal", line=dict(color='#ef4444')))
        fig.add_trace(go.Scatter(x=data['timestamp'], y=data['pressure'], name="Pressure", line=dict(color='#3b82f6')))
        fig.update_layout(height=400, template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("RPM Stability")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = curr['rpm'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {'axis': {'range': [1000, 2000]}, 'bar': {'color': "#1e3a8a"}}
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
