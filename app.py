import streamlit as st
import pandas as pd

# --- CONFIG & THEME ---
st.set_page_config(page_title="ME-PRO | Industrial Suite", layout="wide")

# Professional Color Palette
ACCENT_GOLD = "#D4AF37"
DEEP_BLACK = "#1A1A1A"
OFF_WHITE = "#F4F4F4"
BORD_COLOR = "#E0E0E0"

# --- ADVANCED UI INJECTION ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono&display=swap');
    
    /* Global Styles */
    .stApp {{ background-color: {OFF_WHITE}; font-family: 'Inter', sans-serif; }}
    
    /* Header Container */
    .hero-section {{
        background: linear-gradient(135deg, {DEEP_BLACK} 0%, #333333 100%);
        padding: 60px 20px;
        border-radius: 12px;
        margin-bottom: 40px;
        border-left: 10px solid {ACCENT_GOLD};
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}
    .hero-title {{ color: white !important; font-weight: 900; font-size: 3.2rem; margin: 0; letter-spacing: -1px; }}
    .hero-subtitle {{ color: {ACCENT_GOLD} !important; font-weight: 400; font-size: 1.2rem; opacity: 0.9; }}

    /* Result Cards */
    .result-card {{
        background: white;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid {BORD_COLOR};
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }}
    .metric-val {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #B22222; /* Industrial Red */
    }}
    .metric-lbl {{ font-size: 0.9rem; font-weight: 700; color: #666; text-transform: uppercase; }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (INPUT SETTINGS) ---
with st.sidebar:
    st.markdown("## ⚙️ SYSTEM SETTINGS")
    tool_type = st.radio("ACTIVE MODULE", ["Material Density", "Unit Converter"])
    st.divider()
    
    if tool_type == "Material Density":
        mat_list = {
            "Mild Steel": 7850, "Stainless Steel": 8000, "Aluminum (6061)": 2710,
            "Copper": 8960, "Titanium": 4430, "Cast Iron": 7200, "Brass": 8470
        }
        mat = st.selectbox("BASE MATERIAL", list(mat_list.keys()))
        rho = mat_list[mat]
        
        st.markdown("### GEOMETRY")
        shape = st.radio("SHAPE", ["Block", "Cylinder"])
        
        if shape == "Block":
            l = st.number_input("L (mm)", value=100.0, step=1.0)
            w = st.number_input("W (mm)", value=50.0, step=1.0)
            h = st.number_input("H (mm)", value=10.0, step=1.0)
            vol = (l * w * h) / 1e9
        else:
            dia = st.number_input("Ø Diameter (mm)", value=20.0)
            length = st.number_input("Length (mm)", value=200.0)
            vol = (3.14159 * (dia/2)**2 * length) / 1e9
    else:
        mode = st.selectbox("CATEGORY", ["Stress (MPa)", "Force (N)", "Length (mm)"])
        val = st.number_input("MAGNITUDE", value=1.0, step=0.1)

# --- MAIN DASHBOARD ---
st.markdown(f"""
    <div class="hero-section">
        <p class="hero-subtitle">MECHANICAL ENGINEERING SUITE</p>
        <h1 class="hero-title">ABDUL RAFAY KHAN</h1>
        <p style="color: rgba(255,255,255,0.6); margin-top:10px;">Reg ID: 25-ME-220 | Design Challenge 2026</p>
    </div>
""", unsafe_allow_html=True)

col_main, col_viz = st.columns([2, 1])

with col_main:
    st.markdown(f"### 📊 Analysis Output: {tool_type}")
    
    if tool_type == "Material Density":
        mass = rho * vol
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div class="result-card"><p class="metric-lbl">Total Mass (kg)</p>
                        <p class="metric-val">{mass:.4f}</p></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="result-card"><p class="metric-lbl">Density (kg/m³)</p>
                        <p class="metric-val" style="color:{DEEP_BLACK}">{rho}</p></div>""", unsafe_allow_html=True)
        
        st.info(f"Analysis finalized for **{mat}** profile.")
        
    else:
        if mode == "Stress (MPa)":
            res1, res2, lbl1, lbl2 = val * 145.038, val * 10, "PSI", "Bar"
        elif mode == "Force (N)":
            res1, res2, lbl1, lbl2 = val/1000, val * 0.2248, "kN", "lbf"
        else:
            res1, res2, lbl1, lbl2 = val / 25.4, val / 1000, "Inches", "Meters"
        
        st.markdown(f"""<div class="result-card"><p class="metric-lbl">{lbl1}</p><p class="metric-val">{res1:.2f}</p></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="result-card"><p class="metric-lbl">{lbl2}</p><p class="metric-val">{res2:.4f}</p></div>""", unsafe_allow_html=True)

with col_viz:
    st.markdown("### 🔍 System Info")
    chart_data = pd.DataFrame({"Param": ["Input", "Output"], "Value": [1, 1.5]})
    st.bar_chart(chart_data, x="Param", y="Value")
    st.caption("Real-time simulation status: ACTIVE")

# --- FOOTER ---
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #999;'>Industrial Grade Engine v2.0 | Standardized for UET Engineering Workflows</p>", unsafe_allow_html=True)
