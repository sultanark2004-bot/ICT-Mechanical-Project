"""
Monitoring Page - Real-time System Monitoring
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

def render_monitoring_page(data):
    """Render the real-time monitoring page"""
    
    st.title("🔧 Real-Time System Monitoring")
    st.markdown("---")
    
    # Monitoring tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌡️ Mechanical Sensors",
        "💻 ICT Systems",
        "📊 Live Dashboard",
        "🔔 Alerts & Notifications"
    ])
    
    with tab1:
        render_mechanical_monitoring(data)
    
    with tab2:
        render_ict_monitoring(data)
    
    with tab3:
        render_live_dashboard(data)
    
    with tab4:
        render_alerts(data)

def render_mechanical_monitoring(data):
    """Render mechanical systems monitoring"""
    st.subheader("🌡️ Mechanical Sensors Monitoring")
    
    # Real-time metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_temp = data['temperature'].iloc[-1]
        temp_delta = current_temp - data['temperature'].mean()
        temp_status = "🟢" if abs(temp_delta) < 5 else "🟡"
        
        st.markdown(f"""
            <div class="card" style="text-align: center;">
                <h3>{temp_status} Temperature</h3>
                <h1 style="font-size: 2.5rem; color: #ef4444;">{current_temp:.1f}°F</h1>
                <p style="color: #6b7280;">Delta: {temp_delta:+.1f}°F</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        current_pressure = data['pressure'].iloc[-1]
        pressure_delta = current_pressure - data['pressure'].mean()
        pressure_status = "🟢" if abs(pressure_delta) < 10 else "🟡"
        
        st.markdown(f"""
            <div class="card" style="text-align: center;">
                <h3>{pressure_status} Pressure</h3>
                <h1 style="font-size: 2.5rem; color: #3b82f6;">{current_pressure:.1f} PSI</h1>
                <p style="color: #6b7280;">Delta: {pressure_delta:+.1f} PSI</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        current_rpm = data['rpm'].iloc[-1]
        rpm_delta = current_rpm - data['rpm'].mean()
        rpm_status = "🟢" if abs(rpm_delta) < 100 else "🟡"
        
        st.markdown(f"""
            <div class="card" style="text-align: center;">
                <h3>{rpm_status} RPM</h3>
                <h1 style="font-size: 2.5rem; color: #10b981;">{current_rpm:.0f}</h1>
                <p style="color: #6b7280;">Delta: {rpm_delta:+.0f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        current_vibration = data['vibration'].iloc[-1]
        vibration_delta = current_vibration - data['vibration'].mean()
        vibration_status = "🟢" if current_vibration < 0.6 else "🟡"
        
        st.markdown(f"""
            <div class="card" style="text-align: center;">
                <h3>{vibration_status} Vibration</h3>
                <h1 style="font-size: 2.5rem; color: #f59e0b;">{current_vibration:.2f}</h1>
                <p style="color: #6b7280;">Delta: {vibration_delta:+.2f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Real-time charts
    st.subheader("📊 Live Sensor Data")
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Temperature', 'Pressure', 'RPM', 'Vibration'),
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # Temperature
    fig.add_trace(
        go.Scatter(
            x=data['timestamp'].tail(50),
            y=data['temperature'].tail(50),
            name='Temperature',
            line=dict(color='#ef4444', width=2),
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.1)'
        ),
        row=1, col=1
    )
    
    # Pressure
    fig.add_trace(
        go.Scatter(
            x=data['timestamp'].tail(50),
            y=data['pressure'].tail(50),
            name='Pressure',
            line=dict(color='#3b82f6', width=2),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.1)'
        ),
        row=1, col=2
    )
    
    # RPM
    fig.add_trace(
        go.Scatter(
            x=data['timestamp'].tail(50),
            y=data['rpm'].tail(50),
            name='RPM',
            line=dict(color='#10b981', width=2),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ),
        row=2, col=1
    )
    
    # Vibration
    fig.add_trace(
        go.Scatter(
            x=data['timestamp'].tail(50),
            y=data['vibration'].tail(50),
            name='Vibration',
            line=dict(color='#f59e0b', width=2),
            fill='tozeroy',
            fillcolor='rgba(245, 158, 11, 0.1)'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        template='plotly_white',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Sensor health table
    st.subheader("🔍 Sensor Health Status")
    
    sensor_health = pd.DataFrame({
        'Sensor': ['Temperature Sensor #1', 'Pressure Sensor #2', 'RPM Sensor #3', 'Vibration Sensor #4'],
        'Status': ['🟢 Online', '🟢 Online', '🟢 Online', '🟡 Warning'],
        'Last Reading': [
            f"{data['temperature'].iloc[-1]:.1f}°F",
            f"{data['pressure'].iloc[-1]:.1f} PSI",
            f"{data['rpm'].iloc[-1]:.0f}",
            f"{data['vibration'].iloc[-1]:.2f}"
        ],
        'Health Score': ['98%', '97%', '99%', '85%'],
        'Last Calibration': ['2024-04-15', '2024-04-12', '2024-04-18', '2024-03-20']
    })
    
    st.dataframe(sensor_health, use_container_width=True, hide_index=True)

def render_ict_monitoring(data):
    """Render ICT systems monitoring"""
    st.subheader("💻 ICT Infrastructure Monitoring")
    
    # System metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_cpu = data['cpu_usage'].iloc[-1]
        cpu_status = "🟢" if current_cpu < 70 else ("🟡" if current_cpu < 85 else "🔴")
        
        st.markdown(f"""
            <div class="card" style="text-align: center;">
                <h3>{cpu_status} CPU Usage</h3>
                <h1 style="font-size: 2.5rem; color: #8b5cf6;">{current_cpu:.1f}%</h1>
                <div style="background: #e0e7ff; height: 10px; border-radius: 5px; margin-top: 1rem;">
                    <div style="background: #8b5cf6; height: 10px; border-radius: 5px; width: {current_cpu}%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        current_memory = data['memory_usage'].iloc[-1]
        memory_status = "🟢" if current_memory < 75 else ("🟡" if current_memory < 90 else "🔴")
        
        st.markdown(f"""
            <div class="card" style="text-align: center;">
                <h3>{memory_status} Memory Usage</h3>
                <h1 style="font-size: 2.5rem; color: #06b6d4;">{current_memory:.1f}%</h1>
                <div style="background: #cffafe; height: 10px; border-radius: 5px; margin-top: 1rem;">
                    <div style="background: #06b6d4; height: 10px; border-radius: 5px; width: {current_memory}%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        current_network = data['network_throughput'].iloc[-1]
        network_status = "🟢" if current_network > 75 else ("🟡" if current_network > 50 else "🔴")
        
        st.markdown(f"""
            <div class="card" style="text-align: center;">
                <h3>{network_status} Network Throughput</h3>
                <h1 style="font-size: 2.5rem; color: #10b981;">{current_network:.1f}%</h1>
                <div style="background: #d1fae5; height: 10px; border-radius: 5px; margin-top: 1rem;">
                    <div style="background: #10b981; height: 10px; border-radius: 5px; width: {current_network}%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Network monitoring chart
    st.subheader("📡 Network Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_network = go.Figure()
        
        fig_network.add_trace(go.Scatter(
            x=data['timestamp'].tail(50),
            y=data['network_throughput'].tail(50),
            name='Throughput',
            line=dict(color='#10b981', width=2),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.2)'
        ))
        
        # Add threshold line
        fig_network.add_hline(
            y=75,
            line_dash="dash",
            line_color="red",
            annotation_text="Min Threshold"
        )
        
        fig_network.update_layout(
            title='Network Throughput Trend',
            xaxis_title='Time',
            yaxis_title='Throughput (%)',
            template='plotly_white',
            height=300
        )
        
        st.plotly_chart(fig_network, use_container_width=True)
    
    with col2:
        # Create resource usage comparison
        fig_resources = go.Figure()
        
        fig_resources.add_trace(go.Scatter(
            x=data['timestamp'].tail(50),
            y=data['cpu_usage'].tail(50),
            name='CPU',
            line=dict(color='#8b5cf6', width=2)
        ))
        
        fig_resources.add_trace(go.Scatter(
            x=data['timestamp'].tail(50),
            y=data['memory_usage'].tail(50),
            name='Memory',
            line=dict(color='#06b6d4', width=2)
        ))
        
        fig_resources.update_layout(
            title='Resource Utilization',
            xaxis_title='Time',
            yaxis_title='Usage (%)',
            template='plotly_white',
            height=300
        )
        
        st.plotly_chart(fig_resources, use_container_width=True)
    
    # Connection status
    st.subheader("🌐 Network Devices")
    
    devices = pd.DataFrame({
        'Device': ['Router-01', 'Switch-01', 'Server-01', 'Sensor Gateway', 'Data Logger'],
        'IP Address': ['192.168.1.1', '192.168.1.2', '192.168.1.10', '192.168.1.50', '192.168.1.100'],
        'Status': ['🟢 Online', '🟢 Online', '🟢 Online', '🟢 Online', '🟡 High Latency'],
        'Uptime': ['99.9%', '99.8%', '99.7%', '99.5%', '98.2%'],
        'Last Seen': ['Now', 'Now', 'Now', '1 min ago', '2 min ago']
    })
    
    st.dataframe(devices, use_container_width=True, hide_index=True)

def render_live_dashboard(data):
    """Render comprehensive live dashboard"""
    st.subheader("📊 Live System Dashboard")
    
    # Overall system health
    overall_health = np.random.uniform(88, 96)
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    color: white; padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;">
            <h2 style="margin: 0;">Overall System Health</h2>
            <h1 style="font-size: 4rem; margin: 1rem 0;">{overall_health:.1f}%</h1>
            <p style="font-size: 1.2rem;">All systems operational</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Multi-parameter gauge dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=data['temperature'].iloc[-1],
            title={'text': "Temperature (°F)"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#ef4444"},
                'steps': [
                    {'range': [0, 80], 'color': "#d1fae5"},
                    {'range': [80, 90], 'color': "#fef3c7"},
                    {'range': [90, 100], 'color': "#fecaca"}
                ],
            }
        ))
        fig1.update_layout(height=250)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=data['rpm'].iloc[-1],
            title={'text': "RPM"},
            gauge={
                'axis': {'range': [None, 2000]},
                'bar': {'color': "#3b82f6"},
                'steps': [
                    {'range': [0, 1400], 'color': "#dbeafe"},
                    {'range': [1400, 1600], 'color': "#bfdbfe"},
                    {'range': [1600, 2000], 'color': "#93c5fd"}
                ],
            }
        ))
        fig2.update_layout(height=250)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col3:
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=data['network_throughput'].iloc[-1],
            title={'text': "Network (%)"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#10b981"},
                'steps': [
                    {'range': [0, 50], 'color': "#fecaca"},
                    {'range': [50, 75], 'color': "#fef3c7"},
                    {'range': [75, 100], 'color': "#d1fae5"}
                ],
            }
        ))
        fig3.update_layout(height=250)
        st.plotly_chart(fig3, use_container_width=True)
    
    # Recent activity log
    st.subheader("📝 Recent Activity Log")
    
    activity_log = pd.DataFrame({
        'Timestamp': [
            (datetime.now() - timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S")
            for i in range(10)
        ],
        'Event': [
            'System health check completed',
            'Temperature reading: Normal',
            'Network throughput optimized',
            'Sensor calibration verified',
            'Data backup completed',
            'RPM monitoring: Stable',
            'CPU usage: Normal',
            'Memory usage: Acceptable',
            'Alert resolved: Vibration',
            'System startup completed'
        ],
        'Type': ['✅ Info', '✅ Info', '✅ Success', '✅ Info', '✅ Success', 
                 '✅ Info', '✅ Info', '⚠️ Warning', '✅ Success', '✅ Info']
    })
    
    st.dataframe(activity_log, use_container_width=True, hide_index=True)

def render_alerts(data):
    """Render alerts and notifications"""
    st.subheader("🔔 Alerts & Notifications")
    
    # Active alerts
    st.markdown("### Active Alerts")
    
    active_alerts = pd.DataFrame({
        'Severity': ['⚠️ Warning', '⚠️ Warning', 'ℹ️ Info'],
        'Component': ['Vibration Sensor #4', 'Network Latency', 'Scheduled Maintenance'],
        'Message': [
            'Vibration levels slightly elevated',
            'Network latency increased by 15ms',
            'Maintenance scheduled for May 15, 2026'
        ],
        'Time': ['5 minutes ago', '12 minutes ago', '1 hour ago'],
        'Action': ['Monitor', 'Monitor', 'Acknowledged']
    })
    
    st.dataframe(active_alerts, use_container_width=True, hide_index=True)
    
    # Alert history
    st.markdown("### Alert History (Last 24 Hours)")
    
    alert_history = pd.DataFrame({
        'Timestamp': [
            (datetime.now() - timedelta(hours=i)).strftime("%Y-%m-%d %H:%M")
            for i in range(1, 8)
        ],
        'Severity': ['✅ Resolved', '✅ Resolved', '⚠️ Warning', '✅ Resolved', 
                     'ℹ️ Info', '✅ Resolved', 'ℹ️ Info'],
        'Message': [
            'High temperature alert resolved',
            'Network connectivity restored',
            'CPU usage spike detected',
            'Pressure sensor recalibrated',
            'System update available',
            'Memory usage normalized',
            'Backup completed successfully'
        ]
    })
    
    st.dataframe(alert_history, use_container_width=True, hide_index=True)
    
    # Notification settings
    st.markdown("### Notification Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Email notifications", value=True)
        st.checkbox("SMS alerts for critical events", value=True)
        st.checkbox("Desktop notifications", value=False)
    
    with col2:
        st.checkbox("Daily summary report", value=True)
        st.checkbox("Weekly performance digest", value=True)
        st.checkbox("Maintenance reminders", value=True)
