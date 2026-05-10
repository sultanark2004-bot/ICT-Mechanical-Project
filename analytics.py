import streamlit as st
import plotly.express as px
from sklearn.ensemble import IsolationForest

def render_analytics_page(data):
    st.header("📊 Advanced Engineering Analytics")
    
    # AI Anomaly Detection
    model = IsolationForest(contamination=0.05)
    features = ['temperature', 'vibration', 'pressure', 'rpm']
    data['anomaly'] = model.fit_predict(data[features])
    anomalies = data[data['anomaly'] == -1]

    st.subheader("🤖 Machine Learning Insights")
    if len(anomalies) > 0:
        st.error(f"Detected {len(anomalies)} potential mechanical irregularities!")
    
    # Correlation Heatmap
    corr = data[features].corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', title="Sensor Interdependency")
    st.plotly_chart(fig_corr, use_container_width=True)

    # Vibration vs RPM
    st.subheader("Vibration Analysis (Isolation Forest)")
    fig_anom = px.scatter(data, x="rpm", y="vibration", color="anomaly", 
                         color_discrete_map={1: '#1e3a8a', -1: '#ef4444'},
                         title="Red points indicate system anomalies")
    st.plotly_chart(fig_anom, use_container_width=True)
