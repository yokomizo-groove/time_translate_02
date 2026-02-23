from io import BytesIO
import streamlit as st

import io
import pandas as pd



def download_file(df):

    st.write("Download File ...")
    
    output = BytesIO()
    df.to_excel(output, index=False, engine="xlsxwriter")
    output.seek(0)
    return output

def to_excel_xlsxwriter(df):
    output = io.BytesIO()

    # xlsxwriter をエンジンとして使う
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        # writer.save() は不要（with が自動でやる）

    return output.getvalue()


