import streamlit as st
import os

from load_file import load_file
from time_translate_03 import time_translate
from download_file import download_file


def main():
    st.title("勤怠データチェックアプリ")

    uploaded_file = st.file_uploader(
        "CSVまたはExcelファイルをアップロードしてください",
        type=["csv", "xlsx", "xlsm"]
    )

    if uploaded_file is not None:
        st.success("ファイルを読み込みました")

        df = load_file(uploaded_file)

        st.write("df.shape:", df.shape)

        st.write("Translating time to numerics ...")
        df2 = time_translate(df)
        result_file = download_file(df2)

        base_name = os.path.splitext(uploaded_file.name)[0]
        download_name = f"{base_name}_output.xlsx"

        st.download_button(
            label="変換ファイルをダウンロード",
            data=result_file,
            file_name=download_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


if __name__ == "__main__":
    main()







