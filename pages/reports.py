import streamlit as st
import pandas as pd
from datetime import datetime
import io

def render_reports_page(data):
    st.header("📋 System Audit Reports")
    
    col1, col2 = st.columns(2)
    with col1:
        report_type = st.selectbox("Report Context", ["Mechanical", "ICT", "Full Audit"])
    with col2:
        file_format = st.selectbox("Format", ["Excel", "CSV", "JSON"])

    st.divider()
    st.write("### Preview of Audit Trail")
    st.dataframe(data.tail(15), use_container_width=True)

    # Professional Download Logic
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    if file_format == "Excel":
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False)
        st.download_button("📥 Download Official Report", data=buffer.getvalue(), 
                         file_name=f"Nexus_Report_{timestamp}.xlsx")
    else:
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Data Log", data=csv, 
                         file_name=f"Nexus_Log_{timestamp}.csv")
