import streamlit as st
import os
import io
import pandas as pd
import time

from load_file import load_file
from time_translate_04 import time_translate
from download_file import to_excel_fast_numpy, to_csv_fast


def main():
    st.title("勤怠データチェックアプリ")

    uploaded_file = st.file_uploader(
        "CSVまたはExcelファイルをアップロードしてください",
        type=["csv", "xlsx", "xlsm"]
    )

    if uploaded_file is None:
        return

    st.success("ファイルを読み込みました")

    start = time.time()

    df = load_file(uploaded_file)
    st.write("df.shape:", df.shape)

    st.write("Translating time to numerics ...")
    final_array, headers = time_translate(df)

    # ★ 出力形式を選択
    output_type = st.radio(
        "出力形式を選んでください",
        ("Excel（xlsx）", "CSV"),
        horizontal=True
    )

    base_name = os.path.splitext(uploaded_file.name)[0]

    if output_type == "Excel（xlsx）":
        st.write("Making Excel file ...")
        excel_bytes = to_excel_fast_numpy(final_array, headers)

        st.download_button(
            label="Excelでダウンロード",
            data=excel_bytes,
            file_name=f"{base_name}_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.write("Making CSV file ...")
        csv_bytes = to_csv_fast(final_array, headers)

        st.download_button(
            label="CSVでダウンロード",
            data=csv_bytes,
            file_name=f"{base_name}_output.csv",
            mime="text/csv"
        )

    end = time.time()
    st.info(f"処理時間: {end - start:.2f} 秒")


if __name__ == "__main__":
    main()
