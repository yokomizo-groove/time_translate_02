import pandas as pd
import numpy as np

def fast_convert(series):
    # 文字列化
    s = series.fillna("").astype(str).str.strip()

    # 秒がある場合は切り捨て（"HH:MM:SS" → "HH:MM"）
    s = s.str.slice(0, 5)

    # "H:MM" の場合はゼロ埋め
    s = s.str.replace(r'^(\d):', r'0\1:', regex=True)

    # "HH:MM" → HHMM の整数化
    return (s.str.slice(0, 2).astype(int) * 100 +
            s.str.slice(3, 5).astype(int))

def time_translate(df):

    df = df.copy()
    df.columns = df.columns.str.strip()

    mapping = {
        99: "法定内超勤時間",
        100: "早出残業時間",
        101: "普通残業時間",
        102: "実労働時間",
        103: "所定内深夜時間",
        104: "所定外深夜時間",
        106: "所定外勤務時間",
        107: "休日深夜時間",
        108: "乖離時間(開始)",
        109: "乖離時間(終了)",
        110: "年休換算時間",
        111: "調休換算時間",
        112: "不就業１時間",
        113: "所定内労働時間",
        114: "休憩時間",
        115: "特休勤務時間",
        116: "公休勤務時間",
        121: "出勤打刻",
        122: "退勤打刻",
        123: "始業時刻",
        124: "終業時刻",
    }

    # 150列固定の DataFrame を作る
    MAX_COL = 150
    out = pd.DataFrame("", index=df.index, columns=range(MAX_COL))

    # 元の列を左側にコピー
    for i, col in enumerate(df.columns):
        out[i] = df[col]

    # 時刻変換
    for excel_col, col_name in mapping.items():
        if col_name in df.columns:
            out[excel_col - 1] = fast_convert(df[col_name])

    # 深夜時間計
    if "所定内深夜時間" in df.columns and "所定外深夜時間" in df.columns:
        out[105 - 1] = fast_convert(df["所定内深夜時間"]) + fast_convert(df["所定外深夜時間"])

    # ヘッダー設定
    headers = list(df.columns) + [""] * (MAX_COL - len(df.columns))
    for excel_col, col_name in mapping.items():
        headers[excel_col - 1] = col_name + "-t"
    headers[105 - 1] = "深夜時間計-t"

    out.columns = headers

    return out
