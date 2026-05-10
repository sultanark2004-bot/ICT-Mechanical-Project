import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ME-PRO | Abdul Rafay Khan",
    layout="wide"
)

# --- MAXIMUM CONTRAST CSS ---
st.markdown("""
    <style>
    /* Force Light Mode for Maximum Legibility */
    .stApp { background-color: #FFFFFF; color: #000000; }
    
    /* Extreme Contrast Header */
    .dev-header {
        background-color: #000000;
        padding: 40px;
        border-radius: 0px;
        text-align: center;
        margin-bottom: 30px;
    }
    .dev-header h1 { color: #FFFFFF !important; font-size: 4rem !important; font-weight: 900 !important; margin: 0; }
    .dev-header h2 { color: #FFD700 !important; font-size: 2rem !important; margin: 10px 0; }
    
    /* Bold Metric Styling */
    [data-testid="stMetricValue"] {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: #0000FF !important; /* Bold Blue for results */
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }

    /* Input Labels */
    label p {
        font-size: 1.2rem !important;
        font-weight: bold !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- THE IDENTIFICATION BLOCK (BLACK & GOLD) ---
st.markdown(f"""
    <div class="dev-header">
        <h1>ABDUL RAFAY KHAN</h1>
        <h2>ROLL NO: 25-ME-220</h2>
    </div>
    """, unsafe_allow_html=True)

# --- DATA ---
materials = {
    "Mild Steel": 7850, "Stainless Steel": 8000, "Aluminum (6061)": 2710,
    "Copper": 8960, "Titanium": 4430, "Cast Iron": 7200, "Brass": 8470
}

# --- MAIN INTERFACE ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("### 🛠️ INPUT SETTINGS")
    
    tool_type = st.selectbox("SELECT TOOL", ["Material Density Checker", "Unit Converter"])
    st.divider()

    if tool_type == "Material Density Checker":
        mat = st.selectbox("1. Choose Material", list(materials.keys()))
        rho = materials[mat]
        
        shape = st.radio("2. Geometry", ["Rectangular Block", "Cylinder"])
        if shape == "Rectangular Block":
            l = st.number_input("Length (mm)", value=100.0)
            w = st.number_input("Width (mm)", value=50.0)
            h = st.number_input("Height (mm)", value=10.0)
            vol = (l * w * h) / 1e9
        else:
            dia = st.number_input("Diameter (mm)", value=20.0)
            length = st.number_input("Length (mm)", value=200.0)
            vol = (3.14159 * (dia/2)**2 * length) / 1e9
            
    else:
        mode = st.selectbox("Category", ["Stress (MPa)", "Force (N)", "Length (mm)"])
        val = st.number_input("Enter Magnitude", value=1.0)

with col_right:
    st.markdown("### ✅ RESULTS")
    
    if tool_type == "Material Density Checker":
        mass = rho * vol
        st.metric("SELECTED DENSITY", f"{rho} kg/m³")
        st.metric("CALCULATED MASS", f"{mass:.4f} kg")
        st.metric("MASS IN GRAMS", f"{mass*1000:.1f} g")
        
        st.markdown(f"**Current Material Focus:** {mat}")
        
    else:
        if mode == "Stress (MPa)":
            st.metric("PSI (Pounds/sq in)", f"{val * 145.038:.2f}")
            st.metric("Bar", f"{val * 10:.2f}")
        elif mode == "Force (N)":
            st.metric("kN (Kilonewtons)", f"{val/1000:.4f}")
            st.metric("lbf (Pounds-force)", f"{val * 0.2248:.2f}")
        else:
            st.metric("Inches", f"{val / 25.4:.3f}")
            st.metric("Meters", f"{val / 1000:.4f}")

# --- FOOTER ---
st.markdown("---")
st.caption("Industrial Grade Mechanical Engineering Calculator | High-Contrast Visibility Mode")
