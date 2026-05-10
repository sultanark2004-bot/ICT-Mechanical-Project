import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Mechanical Converter & Density Checker",
    page_icon="🔧",
    layout="wide"
)

# Professional UI/UX Styling
def apply_custom_theme():
    st.markdown("""
        <style>
        /* Main background and font */
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
        
        .main {
            background-color: #0e1117;
        }
        
        /* Glassmorphism Header */
        .header-box {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            margin-bottom: 30px;
        }
        
        .student-info {
            color: #667eea;
            font-family: 'Roboto Mono', monospace;
            font-size: 1.2rem;
            font-weight: bold;
        }

        /* Unit Converter Cards */
        div[data-testid="stVerticalBlock"] > div:has(div.converter-card) {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            padding: 20px;
            border-left: 5px solid #764ba2;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #1a1c24;
        }
        </style>
    """, unsafe_allow_html=True)

# Application Logic
def main():
    apply_custom_theme()

    # --- HEADER SECTION ---
    st.markdown("""
        <div class="header-box">
            <h1 style='color: white; margin-bottom: 0;'>🔧 Mechanical Unit & Density Tool</h1>
            <p class="student-info">Developed by: Abdul Rafay Khan | Roll No: 25-ME-220</p>
        </div>
    """, unsafe_allow_html=True)

    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.header("⚙️ Navigation")
        tool_choice = st.radio("Select Tool:", ["Unit Converter", "Material Density Checker"])
        st.divider()
        st.info("Engineering Tool v1.2")

    # --- TOOL 1: UNIT CONVERTER ---
    if tool_choice == "Unit Converter":
        st.subheader("📏 Engineering Unit Converter")
        col1, col2 = st.columns(2)

        with col1:
            category = st.selectbox("Select Measurement:", ["Pressure", "Temperature", "Length"])
            value = st.number_input("Enter Value:", value=1.0, step=0.1)

        with col2:
            if category == "Pressure":
                unit = st.selectbox("Convert From:", ["PSI to Bar", "Bar to PSI", "Pascal to Bar"])
                if unit == "PSI to Bar":
                    res = value * 0.0689476
                    st.success(f"Result: **{res:.4f} Bar**")
                elif unit == "Bar to PSI":
                    res = value * 14.5038
                    st.success(f"Result: **{res:.4f} PSI**")

            elif category == "Temperature":
                unit = st.selectbox("Conversion:", ["Celsius to Fahrenheit", "Fahrenheit to Celsius"])
                if unit == "Celsius to Fahrenheit":
                    res = (value * 9/5) + 32
                    st.success(f"Result: **{res:.2f} °F**")
                else:
                    res = (value - 32) * 5/9
                    st.success(f"Result: **{res:.2f} °C**")

            elif category == "Length":
                unit = st.selectbox("Conversion:", ["Inches to mm", "mm to Inches"])
                res = value * 25.4 if "mm" in unit else value / 25.4
                st.success(f"Result: **{res:.4f} {'mm' if 'mm' in unit else 'in'}**")

    # --- TOOL 2: DENSITY CHECKER ---
    else:
        st.subheader("🧪 Material Density Checker")
        
        # Material Database
        materials = {
            "Steel": 7850,
            "Aluminum": 2700,
            "Copper": 8960,
            "Titanium": 4506,
            "Cast Iron": 7200
        }
        
        selected_mat = st.selectbox("Select Material:", list(materials.keys()))
        density = materials[selected_mat]
        
        st.metric(label=f"Density of {selected_mat}", value=f"{density} kg/m³")
        
        # Volume Calculation
        st.write("---")
        st.write("### Calculate Mass based on Volume")
        volume = st.number_input("Enter Volume (m³):", value=0.1, min_value=0.0)
        mass = density * volume
        st.warning(f"Estimated Mass: **{mass:.2f} kg**")

if __name__ == "__main__":
    main()
