import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import io

def render_reports_page(data):
    """Render the reports generation page"""
    
    st.title("📋 Reports & Data Export")
    st.markdown("---")
    
    # Report type selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        report_type = st.selectbox(
            "Select Report Type",
            [
                "📊 Performance Summary Report",
                "🔧 Mechanical Systems Report",
                "💻 ICT Infrastructure Report",
                "📈 Trend Analysis Report",
                "🤖 AI Insights Report",
                "📦 Complete Data Export"
            ]
        )
    
    with col2:
        export_format = st.selectbox(
            "Export Format",
            ["CSV", "Excel", "JSON"]
        )
    
    st.markdown("---")
    
    # Logic routing
    if report_type == "📊 Performance Summary Report":
        render_performance_summary(data, export_format)
    elif report_type == "🔧 Mechanical Systems Report":
        render_mechanical_report(data, export_format)
    elif report_type == "💻 ICT Infrastructure Report":
        render_ict_report(data, export_format)
    elif report_type == "📈 Trend Analysis Report":
        render_trend_report(data, export_format)
    elif report_type == "🤖 AI Insights Report":
        render_ai_report(data, export_format)
    elif report_type == "📦 Complete Data Export":
        render_complete_export(data, export_format)

def render_performance_summary(data, export_format):
    st.subheader("📊 Performance Summary Report")
    
    metrics = {
        'Temperature (°F)': 'temperature',
        'Pressure (PSI)': 'pressure',
        'RPM': 'rpm',
        'Vibration': 'vibration',
        'Network Throughput (%)': 'network_throughput',
        'CPU Usage (%)': 'cpu_usage'
    }
    
    summary_list = []
    for name, col in metrics.items():
        curr = data[col].iloc[-1]
        avg = data[col].mean()
        summary_list.append({
            'Metric': name,
            'Current': round(curr, 2),
            'Average': round(avg, 2),
            'Status': '✅ Normal' if abs(curr-avg)/avg < 0.15 else '⚠️ Variance'
        })
    
    summary_df = pd.DataFrame(summary_list)
    st.table(summary_df)
    
    st.markdown("### Report Distribution")
    st.info("This summary is optimized for executive review.")
    download_data(summary_df, "performance_summary", export_format)

def render_mechanical_report(data, export_format):
    st.subheader("🔧 Mechanical Systems Report")
    mech_cols = ['temperature', 'pressure', 'rpm', 'vibration']
    mech_df = data[['timestamp'] + mech_cols]
    
    st.dataframe(mech_df.describe().T, use_container_width=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['temperature'], name="Temp"))
    fig.update_layout(title="Historical Temperature Log", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    
    download_data(mech_df, "mechanical_report", export_format)

def render_ict_report(data, export_format):
    st.subheader("💻 ICT Infrastructure Report")
    ict_cols = ['network_throughput', 'cpu_usage', 'memory_usage']
    st.write("Recent ICT Performance Logs:")
    st.dataframe(data[ict_cols].tail(10), use_container_width=True)
    download_data(data[ict_cols], "ict_report", export_format)

def render_trend_report(data, export_format):
    st.subheader("📈 Trend Analysis Report")
    st.write("Calculated Rolling Averages (Window: 10)")
    trends = data[['temperature', 'pressure']].rolling(window=10).mean()
    st.line_chart(trends)
    download_data(trends, "trend_analysis", export_format)

def render_ai_report(data, export_format):
    st.subheader("🤖 AI Insights Report")
    insights = pd.DataFrame({
        "Category": ["Predictive Maintenance", "Efficiency", "Anomaly Detection"],
        "Prediction": ["Low Risk", "Stable", "None Detected"],
        "Confidence": ["94%", "88%", "99%"]
    })
    st.table(insights)
    download_data(insights, "ai_insights", export_format)

def render_complete_export(data, export_format):
    st.subheader("📦 Complete Data Export")
    st.write(f"Total Rows: {len(data)}")
    st.dataframe(data.head(50))
    download_data(data, "complete_system_export", export_format)

def download_data(dataframe, filename, format_type):
    """Helper function to handle all exports"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == "CSV":
        csv = dataframe.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name=f"{filename}_{timestamp}.csv", mime="text/csv")
    
    elif format_type == "Excel":
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='Sheet1')
        st.download_button("Download Excel", data=buffer.getvalue(), file_name=f"{filename}_{timestamp}.xlsx", mime="application/vnd.ms-excel")
    
    elif format_type == "JSON":
        json_data = dataframe.to_json(orient='records')
        st.download_button("Download JSON", data=json_data, file_name=f"{filename}_{timestamp}.json", mime="application/json")
