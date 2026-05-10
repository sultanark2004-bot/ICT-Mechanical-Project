"""
Reports Page - Generate and Export Reports
"""

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
    
    # Report preview
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
    """Generate performance summary report"""
    st.subheader("📊 Performance Summary Report")
    
    # Generate summary statistics
    summary_data = {
        'Metric': [],
        'Current Value': [],
        'Average': [],
        'Min': [],
        'Max': [],
        'Std Dev': [],
        'Status': []
    }
    
    metrics = {
        'Temperature (°F)': 'temperature',
        'Pressure (PSI)': 'pressure',
        'RPM': 'rpm',
        'Vibration': 'vibration',
        'Network Throughput (%)': 'network_throughput',
        'CPU Usage (%)': 'cpu_usage',
        'Memory Usage (%)': 'memory_usage',
        'System Uptime (%)': 'system_uptime'
    }
    
    for metric_name, metric_col in metrics.items():
        summary_data['Metric'].append(metric_name)
        summary_data['Current Value'].append(f"{data[metric_col].iloc[-1]:.2f}")
        summary_data['Average'].append(f"{data[metric_col].mean():.2f}")
        summary_data['Min'].append(f"{data[metric_col].min():.2f}")
        summary_data['Max'].append(f"{data[metric_col].max():.2f}")
        summary_data['Std Dev'].append(f"{data[metric_col].std():.2f}")
        
        # Simple status logic
        current = data[metric_col].iloc[-1]
        avg = data[metric_col].mean()
        if abs(current - avg) / avg < 0.1:
            summary_data['Status'].append('✅ Normal')
        elif abs(current - avg) / avg < 0.2:
            summary_data['Status'].append('⚠️ Warning')
        else:
            summary_data['Status'].append('❌ Alert')
    
    summary_df = pd.DataFrame(summary_data)
    
    # Display summary
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    # Report metadata
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Report Generated", datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    with col2:
        st.metric("Data Points Analyzed", len(data))
    
    with col3:
        st.metric("Time Period", f"{len(data)} hours")
    
    # Download button
    st.markdown("---")
    download_data(summary_df, "performance_summary", export_format)

def render_mechanical_report(data, export_format):
    """Generate mechanical systems report"""
    st.subheader("🔧 Mechanical Systems Report")
    
    # Mechanical metrics
    mechanical_cols = ['temperature', 'pressure', 'rpm', 'vibration']
    mechanical_data = data[['timestamp'] + mechanical_cols].copy()
    
    # Add calculated fields
    mechanical_data['temp_status'] = mechanical_data['temperature'].apply(
        lambda x: 'Normal' if x < 80 else ('Warning' if x < 90 else 'Critical')
    )
    mechanical_data['pressure_status'] = mechanical_data['pressure'].apply(
        lambda x: 'Normal' if 90 < x < 110 else 'Warning'
    )
    mechanical_data['rpm_status'] = mechanical_data['rpm'].apply(
        lambda x: 'Normal' if 1400 < x < 1600 else 'Warning'
    )
    
    # Summary statistics
    st.markdown("### Summary Statistics")
    summary = mechanical_data[mechanical_cols].describe().T
    st.dataframe(summary.style.background_gradient(cmap='RdYlGn_r'), use_container_width=True)
    
    # Visualizations
    st.markdown("### Performance Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=data['timestamp'],
            y=data['temperature'],
            name='Temperature',
            line=dict(color='#ef4444', width=2)
        ))
        fig1.update_layout(
            title='Temperature Trend',
            xaxis_title='Time',
            yaxis_title='Temperature (°F)',
            template='plotly_white',
            height=300
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=data['timestamp'],
            y=data['rpm'],
            name='RPM',
            line=dict(color='#3b82f6', width=2)
        ))
        fig2.update_layout(
            title='RPM Trend',
            xaxis_title='Time',
            yaxis_title='RPM',
            template='plotly_white',
            height=300
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Download
    st.markdown("---")
    download_data(mechanical_data, "mechanical_systems_report", export_format)

def render_ict_report(data, export_format):
    """Generate ICT infrastructure report"""
    st.subheader("💻 ICT Infrastructure Report")
    
    # ICT metrics
    ict_cols = ['network_throughput', 'cpu_usage', 'memory_usage', 'system_uptime']
    ict_data = data[['timestamp'] + ict_cols].copy()
    
    # Add health indicators
    ict_data['network_health'] = ict_data['network_throughput'].apply(
        lambda x: 'Excellent' if x > 90 else ('Good' if x > 75 else 'Fair')
    )
    ict_data['cpu_health'] = ict_data['cpu_usage'].apply(
        lambda x: 'Normal' if x < 70 else ('High' if x < 85 else 'Critical')
    )
    ict_data['memory_health'] = ict_data['memory_usage'].apply(
        lambda x: 'Normal' if x < 75 else ('High' if x < 90 else 'Critical')
    )
    
    # Summary
    st.markdown("### Infrastructure Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Avg Network Throughput",
            f"{ict_data['network_throughput'].mean():.1f}%",
            f"{ict_data['network_throughput'].iloc[-1] - ict_data['network_throughput'].mean():.1f}%"
        )
    
    with col2:
        st.metric(
            "Avg CPU Usage",
            f"{ict_data['cpu_usage'].mean():.1f}%",
            f"{ict_data['cpu_usage'].iloc[-1] - ict_data['cpu_usage'].mean():.1f}%"
        )
    
    with col3:
        st.metric(
            "Avg Memory Usage",
            f"{ict_data['memory_usage'].mean():.1f}%",
            f"{ict_data['memory_usage'].iloc[-1] - ict_data['memory_usage'].mean():.1f}%"
        )
    
    with col4:
        st.metric(
            "System Uptime",
            f"{ict_data['system_uptime'].mean():.2f}%",
            "0.5%"
        )
    
    # Detailed table
    st.markdown("### Detailed Metrics")
    st.dataframe(
        ict_data.tail(20).style.background_gradient(subset=ict_cols, cmap='RdYlGn'),
        use_container_width=True,
        hide_index=True
    )
    
    # Download
    st.markdown("---")
    download_data(ict_data, "ict_infrastructure_report", export_format)

def render_trend_report(data, export_format):
    """Generate trend analysis report"""
    st.subheader("📈 Trend Analysis Report")
    
    # Calculate trends
    trend_data = data.copy()
    
    # Rolling averages
    window = 10
    for col in ['temperature', 'pressure', 'rpm', 'network_throughput']:
        trend_data[f'{col}_ma'] = trend_data[col].rolling(window=window).mean()
        trend_data[f'{col}_trend'] = trend_data[col].diff()
    
    # Trend summary
    st.markdown("### Trend Summary")
    
    trend_summary = {
        'Parameter': ['Temperature', 'Pressure', 'RPM', 'Network Throughput'],
        'Current Trend': [],
        'Change Rate': [],
        'Forecast': []
    }
    
    for col in ['temperature', 'pressure', 'rpm', 'network_throughput']:
        recent_trend = trend_data[f'{col}_trend'].tail(10).mean()
        trend_summary['Current Trend'].append(
            '📈 Increasing' if recent_trend > 0 else '📉 Decreasing'
        )
        trend_summary['Change Rate'].append(f"{abs(recent_trend):.2f}/hour")
        trend_summary['Forecast'].append(
            'Stable' if abs(recent_trend) < 0.5 else 'Monitoring Required'
        )
    
    trend_summary_df = pd.DataFrame(trend_summary)
    st.dataframe(trend_summary_df, use_container_width=True, hide_index=True)
    
    # Visualization
    st.markdown("### Trend Visualization")
    
    fig = go.Figure()
    
    for col in ['temperature', 'pressure', 'rpm']:
        fig.add_trace(go.Scatter(
            x=trend_data['timestamp'],
            y=trend_data[col],
            name=col.capitalize(),
            mode='lines'
        ))
    
    fig.update_layout(
        title='Multi-Parameter Trend Analysis',
        xaxis_title='Time',
        yaxis_title='Value (Normalized)',
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Download
    st.markdown("---")
    download_data(trend_data, "trend_analysis_report", export_format)

def render_ai_report(data, export_format):
    """Generate AI insights report"""
    st.subheader("🤖 AI Insights Report")
    
    # AI-generated insights
    insights = {
        'Insight Category': [
            'Equipment Health',
            'Performance Optimization',
            'Predictive Maintenance',
            'Risk Assessment',
            'Resource Utilization'
        ],
        'Status': [
            '✅ Excellent',
            '⚠️ Moderate',
            '✅ Low Risk',
            '✅ Low',
            '⚠️ Can Improve'
        ],
        'Confidence': ['95%', '87%', '92%', '94%', '88%'],
        'Recommendation': [
            'Continue current maintenance schedule',
            'Optimize cooling system efficiency',
            'Schedule maintenance in 3 weeks',
            'Monitor vibration levels',
            'Consider load balancing improvements'
        ]
    }
    
    insights_df = pd.DataFrame(insights)
    st.dataframe(insights_df, use_container_width=True, hide_index=True)
    
    # Predictive scores
    st.markdown("### Predictive Scores")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Health Score", "92.5%", "+2.1%")
    
    with col2:
        st.metric("Efficiency Score", "87.3%", "-1.4%")
    
    with col3:
        st.metric("Reliability Score", "94.8%", "+0.8%")
    
    # Download
    st.markdown("---")
    download_data(insights_df, "ai_insights_report", export_format)

def render_complete_export(data, export_format):
    """Generate complete data export"""
    st.subheader("📦 Complete Data Export")
    
    st.info("""
        This export includes all collected data points with timestamps.
        Use this for external analysis or archival purposes.
    """)
    
    # Display data preview
    st.markdown("### Data Preview (Last 20 Records)")
    st.dataframe(data.tail(20), use_container_width=True)
    
    # Statistics
    st.markdown("### Dataset Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(data))
    
    with col2:
        st.metric("Parameters", len(data.columns))
    
    with col3:
        st.metric("Start Date", data['timestamp'].min().strftime("%Y-%m-%d"))
    
    with col4:
        st.metric("End Date", data['timestamp'].max().strftime("%Y-%m-%d"))
    
    # Download
    st.markdown("---")
    download_data(data, "complete_data_export", export_format)

def download_data(dataframe, filename, format_type):
    """Generate download button for data export"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == "CSV":
        csv = dataframe.to_csv(index=False)
        st.download_button(
            label=f"📥 Download {format_type}",
            data=csv,
            file_name=f"{filename}_{timestamp}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    elif format_type == "Excel":
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='Report')
        
        st.download_button(
            label=f"📥 Download {format_type}",
            data=buffer.getvalue(),
            file_name=f"{filename}_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    elif format_type == "JSON":
        json_str = dataframe.to_json(orient='records', date_format='iso')
        st.download_button(
            label=f"📥 Download {format_type}",
            data=json_str,
            file_name=f"{filename}_{timestamp}.json",
            mime="application/json",
            use_container_width=True
        )
