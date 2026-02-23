from io import BytesIO
import streamlit as st

st.write("Download File ...")

def download_file(df):
    output = BytesIO()
    df.to_excel(output, index=False, engine="xlsxwriter")
    output.seek(0)
    return output

