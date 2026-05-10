import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- UI Setup ---
st.set_page_config(page_title="Advanced Mechanical Suite", layout="wide")

# Header with IDs
st.sidebar.markdown(f"## System Information")
st.sidebar.info(f"**Lead Engineer:** Abdul Rafay Khan\n\n**ID:** 25-ME-220")

st.title("🚀 Advanced Mechanical Engineering Suite")
st.markdown("---")

# --- Tabs for Clean Navigation ---
tab1, tab2, tab3 = st.tabs(["Material Intelligence", "Unit Converter Pro", "Stress-Strain Simulator"])

# --- TAB 1: MATERIAL INTELLIGENCE ---
with tab1:
    st.header("Material Properties Database")
    
    # Advanced Material Data
    material_data = {
        "Material": ["Steel (AISI 1020)", "Aluminum (6061-T6)", "Titanium (Grade 5)", "Copper (C11000)", "Cast Iron (Gray)"],
        "Density (kg/m³)": [7850, 2700, 4430, 8940, 7200],
        "Young's Modulus (GPa)": [200, 68.9, 114, 117, 110],
        "Yield Strength (MPa)": [350, 276, 880, 70, 240],
        "Thermal Expansion (10⁻⁶/°C)": [11.7, 23.6, 8.6, 16.7, 11.0]
    }
    df = pd.DataFrame(material_data)
    
    selected_mat = st.selectbox("Search & Select Material", df["Material"])
    mat_info = df[df["Material"] == selected_mat].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Density", f"{mat_info['Density (kg/m³)']}", "kg/m³")
    col2.metric("Young's Modulus", f"{mat_info['Young\'s Modulus (GPa)']} GPa")
    col3.metric("Yield Strength", f"{mat_info['Yield Strength (MPa)']} MPa")

# --- TAB 2: UNIT CONVERTER PRO ---
with tab2:
    st.header("High-Precision Conversion")
    col_a, col_b = st.columns(2)
    
    with col_a:
        category = st.selectbox("Category", ["Dynamic Viscosity", "Thermal Conductivity", "Pressure/Stress"])
        input_val = st.number_input("Value to Convert", value=1.0, format="%.4f")
        
    with col_b:
        if category == "Pressure/Stress":
            units = {"MPa": 1, "psi": 145.038, "bar": 10, "ksi": 0.145038}
            base_unit = st.selectbox("From", list(units.keys()))
            # Logic: Convert to MPa then to all others
            val_in_mpa = input_val / units[base_unit]
            st.write("**Equivalent Values:**")
            for u, factor in units.items():
                st.write(f"{u}: `{val_in_mpa * factor:.4f}`")

# --- TAB 3: STRESS-STRAIN SIMULATOR ---
with tab3:
    st.header("Synthetic Stress-Strain Curve")
    st.caption("Visualizing the elastic and plastic deformation based on selected material properties.")
    
    # Generate a theoretical curve using Ramberg-Osgood style logic
    E = mat_info["Young's Modulus (GPa)"] * 1000  # Convert to MPa
    sy = mat_info["Yield Strength (MPa)"]
    
    strain_elastic = np.linspace(0, sy/E, 50)
    stress_elastic = E * strain_elastic
    
    strain_plastic = np.linspace(sy/E, 0.2, 100)
    stress_plastic = sy + (E * 0.05) * (strain_plastic - sy/E)**0.5 # Simplified hardening
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strain_elastic, y=stress_elastic, name='Elastic Region', line=dict(color='blue', width=3)))
    fig.add_trace(go.Scatter(x=strain_plastic, y=stress_plastic, name='Plastic Region', line=dict(color='red', dash='dash')))
    
    fig.update_layout(title=f"Theoretical Curve for {selected_mat}",
                     xaxis_title="Strain (ε)", yaxis_title="Stress (σ) MPa",
                     template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
