import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- ADVANCED UI CONFIGURATION ---
st.set_page_config(
    page_title="MECH-PRO | Advanced Suite",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Branding
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    .developer-box { 
        padding: 20px; 
        border-radius: 10px; 
        background: linear-gradient(135deg, #1e3a8a 0%, #1e1b4b 100%);
        color: white;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR IDENTIFICATION ---
with st.sidebar:
    st.markdown(f"""
    <div class="developer-box">
        <h2 style='margin:0;'>Abdul Rafay Khan</h2>
        <p style='opacity:0.8;'>Reg ID: 25-ME-220</p>
        <hr style='opacity:0.3;'>
        <p style='font-size:0.8rem;'>Mechanical Engineering Systems v3.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Control Panel")
    app_mode = st.radio("Toolbox Selection", 
        ["Material Analytics", "Precision Converter", "Structural Beam Preview"])

# --- DATA ENGINE ---
materials_db = pd.DataFrame({
    "Material": ["Steel (AISI 1020)", "Aluminum (6061-T6)", "Titanium (Gr 5)", "Copper (Pure)", "Brass"],
    "Density (kg/m³)": [7850, 2700, 4430, 8960, 8500],
    "Elastic Modulus (GPa)": [200, 68.9, 114, 117, 100],
    "Yield Strength (MPa)": [350, 276, 880, 70, 200],
    "Thermal Exp (µm/m·K)": [11.7, 23.6, 8.6, 16.7, 18.7]
})

# --- APP LOGIC ---

if app_mode == "Material Analytics":
    st.title("🔬 Material Property Analytics")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_material = st.selectbox("Select Specimen", materials_db["Material"])
        mat_data = materials_db[materials_db["Material"] == selected_material].iloc[0]
        
        st.metric("Density", f"{mat_data['Density (kg/m³)']:,} kg/m³")
        st.metric("Modulus of Elasticity", f"{mat_data['Elastic Modulus (GPa)']} GPa")
        st.metric("Yield Stress", f"{mat_data['Yield Strength (MPa)']} MPa")

    with col2:
        # Comparison Radar Chart
        fig = go.Figure()
        categories = ['Density', 'Elastic Modulus', 'Yield Strength', 'Thermal Exp']
        
        # Normalized values for visual comparison
        fig.add_trace(go.Scatterpolar(
            r=[mat_data['Density (kg/m³)']/9000, mat_data['Elastic Modulus (GPa)']/200, 
               mat_data['Yield Strength (MPa)']/900, mat_data['Thermal Exp (µm/m·K)']/25],
            theta=categories, fill='toself', name=selected_material
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=False)), showlegend=True, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

elif app_mode == "Precision Converter":
    st.title("⚖️ Precision Unit Engine")
    
    # Advanced Converter Logic
    conv_groups = {
        "Pressure/Stress": {"MPa": 1, "psi": 145.038, "Bar": 10, "Pa": 1000000},
        "Force": {"Newton (N)": 1, "kN": 0.001, "lbf": 0.2248},
        "Energy": {"Joule": 1, "BTU": 0.000947, "ft-lb": 0.737}
    }
    
    group = st.selectbox("Category", list(conv_groups.keys()))
    val = st.number_input("Input Magnitude", value=100.0)
    
    cols = st.columns(len(conv_groups[group]))
    for i, (unit, factor) in enumerate(conv_groups[group].items()):
        cols[i].metric(unit, f"{val * factor:,.3f}")

elif app_mode == "Structural Beam Preview":
    st.title("🏗️ Basic Beam Stress Visualization")
    st.info("Visualizing bending stress distribution across a cross-section.")
    
    # Simple Stress Graphing
    y = np.linspace(-50, 50, 100) # Section height
    M = st.slider("Bending Moment (kNm)", 1, 500, 100)
    I = 1e6 # Moment of Inertia constant
    stress = (M * 1000 * y) / I # Sigma = My/I
    
    fig = px.line(x=stress, y=y, labels={'x':'Stress (MPa)', 'y':'Distance from Neutral Axis (mm)'},
                 title="Bending Stress Profile")
    fig.add_vline(x=0, line_dash="dash", line_color="white")
    st.plotly_chart(fig, use_container_width=True)
