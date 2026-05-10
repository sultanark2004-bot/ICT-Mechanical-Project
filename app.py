import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ME-Systems | Abdul Rafay Khan",
    page_icon="⚙️",
    layout="wide"
)

# --- CUSTOM CSS FOR PROFESSIONAL UI ---
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .header-box {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #334155;
        margin-bottom: 25px;
        text-align: center;
    }
    .stMetric {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        padding: 15px !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- IDENTIFICATION HEADER ---
st.markdown(f"""
    <div class="header-box">
        <h1 style="color: #38bdf8; margin: 0;">Mechanical Systems Suite</h1>
        <p style="color: #94a3b8; font-size: 1.2rem; margin: 5px 0;">Developed by: <b>Abdul Rafay Khan</b></p>
        <p style="color: #64748b; font-size: 1rem; margin: 0;">Registration No: <b>25-ME-220</b></p>
    </div>
    """, unsafe_allow_html=True)

# --- DATASET ---
materials = {
    "Mild Steel": 7850,
    "Stainless Steel (304)": 8000,
    "Aluminum (6061)": 2710,
    "Copper (Pure)": 8960,
    "Titanium (Gr 5)": 4430,
    "Cast Iron": 7200,
    "Brass": 8470
}

# --- TOOL NAVIGATION ---
tab1, tab2 = st.tabs(["⚖️ Material Density Checker", "🔄 Precision Unit Converter"])

# --- TAB 1: MATERIAL DENSITY CHECKER ---
with tab1:
    st.header("Material Density & Mass Engine")
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("Input Parameters")
        selected_mat = st.selectbox("Step 1: Select Material", list(materials.keys()))
        density = materials[selected_mat]
        
        shape = st.radio("Step 2: Component Geometry", ["Rectangular Block", "Solid Cylinder", "Custom Volume"])
        
        if shape == "Rectangular Block":
            L = st.number_input("Length (mm)", value=100.0)
            W = st.number_input("Width (mm)", value=50.0)
            H = st.number_input("Height (mm)", value=10.0)
            volume_m3 = (L * W * H) / 1e9
            
        elif shape == "Solid Cylinder":
            D = st.number_input("Diameter (mm)", value=20.0)
            L = st.number_input("Length (mm)", value=200.0)
            volume_m3 = (3.14159 * (D/2)**2 * L) / 1e9
            
        else:
            v_cm3 = st.number_input("Enter Volume (cm³)", value=100.0)
            volume_m3 = v_cm3 / 1e6

    with col2:
        st.subheader("Calculation Result")
        mass_kg = density * volume_m3
        
        res_col1, res_col2 = st.columns(2)
        res_col1.metric("Density", f"{density} kg/m³")
        res_col2.metric("Calculated Mass", f"{mass_kg:.4f} kg")
        
        st.write(f"**Material Profile:** {selected_mat}")
        st.progress(min(mass_kg / 10.0, 1.0)) # Visual bar based on 10kg max
        
        st.success(f"Result: The part weighs **{mass_kg*1000:.2f} grams**.")

# --- TAB 2: PRECISION UNIT CONVERTER ---
with tab2:
    st.header("Mechanical Unit Converter")
    
    cat = st.selectbox("Select Dimension", ["Stress & Pressure", "Force", "Length"])
    val_in = st.number_input("Enter Value", value=1.0, format="%.4f")
    
    st.markdown("---")
    res_cols = st.columns(3)
    
    if cat == "Stress & Pressure":
        # Base is MPa
        res_cols[0].metric("Megapascals (MPa)", f"{val_in:.2f}")
        res_cols[1].metric("PSI (lb/in²)", f"{val_in * 145.038:.2f}")
        res_cols[2].metric("Bar", f"{val_in * 10:.2f}")
        
    elif cat == "Force":
        # Base is Newtons
        res_cols[0].metric("Newtons (N)", f"{val_in:.2f}")
        res_cols[1].metric("Kilonewtons (kN)", f"{val_in / 1000:.4f}")
        res_cols[2].metric("Pounds-force (lbf)", f"{val_in * 0.2248:.2f}")
        
    elif cat == "Length":
        # Base is Millimeters
        res_cols[0].metric("Millimeters (mm)", f"{val_in:.2f}")
        res_cols[1].metric("Inches (in)", f"{val_in / 25.4:.4f}")
        res_cols[2].metric("Meters (m)", f"{val_in / 1000:.4f}")

st.sidebar.markdown("### Documentation")
st.sidebar.write("This tool provides high-accuracy density lookups and unit conversions specifically for Mechanical Engineering students.")
