import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ME-PRO | Abdul Rafay Khan",
    page_icon="⚙️",
    layout="wide"
)

# --- HIGH-VISIBILITY CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main background */
    .stApp { background-color: #0b0e14; }
    
    /* Identification Header */
    .dev-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #1e1b4b 100%);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #3b82f6;
        text-align: center;
        margin-bottom: 30px;
    }
    .dev-header h1 { color: #ffffff !important; font-size: 3rem !important; margin: 0; }
    .dev-header h2 { color: #60a5fa !important; font-size: 1.5rem !important; margin: 5px 0; }
    
    /* Result Cards */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: bold !important;
        color: #10b981 !important;
    }
    
    /* Input Box Styling */
    .stNumberInput, .stSelectbox {
        border: 1px solid #3b82f6 !important;
        border-radius: 5px;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #1f2937;
        border-radius: 5px 5px 0 0;
        color: white;
        padding: 0 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VISIBLE ID HEADER ---
st.markdown(f"""
    <div class="dev-header">
        <h1>Abdul Rafay Khan</h1>
        <h2>Roll No: 25-ME-220</h2>
        <p style="color:white; opacity:0.7;">Mechanical Unit Converter & Density Checker</p>
    </div>
    """, unsafe_allow_html=True)

# --- DATA ---
materials = {
    "Mild Steel": 7850, "Stainless Steel": 8000, "Aluminum (6061)": 2710,
    "Copper": 8960, "Titanium": 4430, "Cast Iron": 7200, "Brass": 8470
}

# --- TABS ---
tab1, tab2 = st.tabs(["📊 MATERIAL DENSITY CHECKER", "🔢 UNIT CONVERTER"])

with tab1:
    st.header("Step 1: Check Density & Calculate Mass")
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("🛠️ Inputs")
        mat = st.selectbox("Select Material Type", list(materials.keys()))
        rho = materials[mat]
        
        shape = st.radio("Geometry Type", ["Block", "Cylinder"])
        if shape == "Block":
            l = st.number_input("Length (mm)", value=100.0)
            w = st.number_input("Width (mm)", value=50.0)
            h = st.number_input("Height (mm)", value=10.0)
            vol = (l * w * h) / 1e9
        else:
            dia = st.number_input("Diameter (mm)", value=20.0)
            length = st.number_input("Length (mm)", value=200.0)
            vol = (3.14159 * (dia/2)**2 * length) / 1e9

    with c2:
        st.subheader("✅ Calculated Results")
        mass = rho * vol
        st.metric("Material Density", f"{rho} kg/m³")
        st.metric("Final Mass (kg)", f"{mass:.4f}")
        st.metric("Final Mass (grams)", f"{mass*1000:.1f}")
        st.info(f"Currently calculating for: **{mat}**")

with tab2:
    st.header("Step 2: Precision Unit Conversion")
    mode = st.selectbox("Category", ["Stress (MPa)", "Force (N)", "Length (mm)"])
    val = st.number_input("Enter Value", value=1.0)
    
    st.markdown("---")
    res1, res2, res3 = st.columns(3)
    
    if mode == "Stress (MPa)":
        res1.metric("MPa", val)
        res2.metric("PSI", round(val * 145.038, 2))
        res3.metric("Bar", round(val * 10, 2))
    elif mode == "Force (N)":
        res1.metric("Newtons", val)
        res2.metric("kN", val/1000)
        res3.metric("lbf", round(val * 0.2248, 2))
    else:
        res1.metric("mm", val)
        res2.metric("Inches", round(val / 25.4, 3))
        res3.metric("Meters", val / 1000)

st.sidebar.success("App Status: Running Stable")
st.sidebar.write("Ensure you are in 'Dark Mode' in Streamlit settings for best visibility.")
