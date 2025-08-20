from streamlit import session_state
def filtered_PK_theo_ten_file_KHTH(tenFileDeXuatHienTai):
    return [item for item in session_state.ten_PK_theo_KHTH_dict if item['file_sheet_name'] == tenFileDeXuatHienTai]
