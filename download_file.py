from io import BytesIO
import streamlit as st



def download_file(df):

    st.write("Download File ...")
    
    output = BytesIO()
    df.to_excel(output, index=False, engine="xlsxwriter")
    output.seek(0)
    return output


