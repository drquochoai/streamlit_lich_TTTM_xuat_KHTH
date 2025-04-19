import streamlit as st
import pandas as pd

def load_excel_data_from_url(url):
    excel_file = pd.ExcelFile(url)
    st.session_state.sheet_names = excel_file.sheet_names  # Store the sheet names in session state.
    all_data = {}
    for sheet_name in excel_file.sheet_names:   # Iterate through all sheets in the Excel file.
        df = excel_file.parse(sheet_name)
        for col in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)
        all_data[sheet_name] = df
        
    return all_data
