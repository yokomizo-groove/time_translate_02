from io import BytesIO


def download_file(df):
    output = BytesIO()
    df.to_excel(output, index=False, engine="xlsxwriter")
    output.seek(0)
    return output
