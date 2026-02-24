from io import BytesIO
import streamlit as st

import io
import pandas as pd



def download_file(df):

    st.write("Making download file ...")    
    
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

def to_excel_fast_numpy(final_array, headers):
    output = io.BytesIO()
    import xlsxwriter

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Sheet1")

    # ヘッダー書き込み
    for col, name in enumerate(headers):
        worksheet.write(0, col, name)

    # データ書き込み（NumPy 配列を直接書く）
    rows, cols = final_array.shape
    for r in range(rows):
        for c in range(cols):
            worksheet.write(r + 1, c, final_array[r, c])

    workbook.close()
    return output.getvalue()





