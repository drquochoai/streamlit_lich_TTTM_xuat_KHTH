import streamlit as st
import pandas as pd
import os
from SETTINGS_FOR_ALL import SETTINGS

@st.cache_data(show_spinner=False)
def load_excel_data_from_url(url):
    """
    Load Excel workbook from URL with a graceful offline fallback:
    - Try URL first.
    - If network fails, try SETTINGS['url']['localFallback'] if provided and exists.
    - Otherwise, surface a friendly error and stop the app to avoid a crash.
    Returns a dict of sheet_name -> DataFrame (all non-datetime columns coerced to str).
    """
    excel_file = None
    # 1) Try network URL
    try:
        excel_file = pd.ExcelFile(url)
    except Exception as e:
        # 2) Try local fallback if configured
        local_fallback = (SETTINGS.get("url", {}) or {}).get("localFallback")
        if local_fallback and os.path.exists(local_fallback):
            excel_file = pd.ExcelFile(local_fallback)
        else:
            raise RuntimeError(
                "Không tải được file Excel từ Internet và không có file localFallback. "
                "Hãy cấu hình SETTINGS['url']['localFallback'] hoặc kiểm tra kết nối mạng."
            )

    # 3) Parse all sheets
    st.session_state.sheet_names = excel_file.sheet_names  # Store the sheet names in session state.
    all_data = {}
    for sheet_name in excel_file.sheet_names:   # Iterate through all sheets in the Excel file.
        df = excel_file.parse(sheet_name)
        for col in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)
        all_data[sheet_name] = df

    return all_data
