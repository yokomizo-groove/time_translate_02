import streamlit as st
import os
import io
import pandas as pd
import time

from load_file import load_file
from time_translate_03 import time_translate


# ★ 高速 xlsxwriter 版 Excel 変換関数
def to_excel_xlsxwriter(df):
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

    

def main():
    st.title("勤怠データチェックアプリ")

    uploaded_file = st.file_uploader(
        "CSVまたはExcelファイルをアップロードしてください",
        type=["csv", "xlsx", "xlsm"]
    )

    if uploaded_file is not None:
        st.success("ファイルを読み込みました")

        # ★ タイマー開始 start = time.time()
        
        df = load_file(uploaded_file)
        st.write("df.shape:", df.shape)

        st.write("Translating time to numerics ...")
        df2 = time_translate(df)

        # ★ ここで Excel バイト列を作る（高速）
        st.write("Making download file with xlsxwriter")
        excel_bytes = to_excel_xlsxwriter(df2)
        
        # ★ タイマー終了
        end = time.time() 
        elapsed = end - start

        # ★ 結果表示
        st.info(f"処理時間: {elapsed:.2f} 秒")
        
        base_name = os.path.splitext(uploaded_file.name)[0]
        download_name = f"{base_name}_output.xlsx"

        # ★ ダウンロードボタン
        st.download_button(
            label="変換ファイルをダウンロード",
            data=excel_bytes,
            file_name=download_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


if __name__ == "__main__":
    main()
