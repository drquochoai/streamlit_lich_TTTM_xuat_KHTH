import streamlit as st
import pandas as pd
from SETTINGS_FOR_ALL import SETTINGS
sheetNamedefault = SETTINGS.get("sheetName", {}).get("phongKham")


@st.cache_data
def xuLyTenDanhSachPK(full_lich, sheetName=sheetNamedefault):
    """
    Xuất danh sách phòng khám theo tên sheet. 🏥Tên PK theo KHTH
    Args:
        full_lich (dict): Danh sách phòng khám theo tên sheet.
    Returns:
        pd.DataFrame: [ {'key': 'value'} ] : Danh sách phòng khám.
        ### array of this: https://i.imgur.com/WkRIQkw.png
    """
    # get data of the sheet default phongKham
    ten_PK_theo_KHTH = full_lich[sheetName]
    # set column 0 as index
    ten_PK_theo_KHTH = ten_PK_theo_KHTH.set_index(ten_PK_theo_KHTH.columns[0])
    # set 1st row as header
    ten_PK_theo_KHTH.columns = ten_PK_theo_KHTH.iloc[0]
    # drop first row (row 0) because it is "code"
    # ten_PK_theo_KHTH = ten_PK_theo_KHTH.iloc[1:]

    # just get row have column 2 (loc 1) != nan in string; Mã theo KHTH (code_KHTH)
    ten_PK_theo_KHTH = ten_PK_theo_KHTH[ten_PK_theo_KHTH.iloc[:, 1] != 'nan']

    # ten_PK_theo_KHTH = drop column if row 1 = 'nan', do not use dropna
    # Identify columns where the first row is 'nan'
    cols_to_drop = ten_PK_theo_KHTH.columns[ten_PK_theo_KHTH.iloc[0] == 'nan']
    # Drop these columns
    ten_PK_theo_KHTH = ten_PK_theo_KHTH.drop(cols_to_drop, axis=1)

    ten_PK_theo_KHTH = ten_PK_theo_KHTH.dropna(axis=1, how='all')
    # drop first row (row 0) because it is "code"
    ten_PK_theo_KHTH = ten_PK_theo_KHTH.iloc[1:]

    # st.write(ten_PK_theo_KHTH.columns)
    # get unique values of column have the name "file_sheet_name"

    ten_PK_theo_KHTH_unique = ten_PK_theo_KHTH["file_sheet_name"].unique()
    st.session_state.ten_PK_theo_KHTH_unique = [
        x for x in ten_PK_theo_KHTH_unique if pd.notna(x) and str(x).lower() != "nan"]
    # sort the list ten_PK_theo_KHTH_unique to be in alphabetical order reverse
    st.session_state.ten_PK_theo_KHTH_unique = sorted(st.session_state.ten_PK_theo_KHTH_unique, reverse=True)
    # st.write("st.session_state.ten_PK_theo_KHTH_unique", st.session_state.ten_PK_theo_KHTH_unique)
    """ 	array		[9]
        0	:	22. PK Nội tim mạch.xlsx
        1	:	1.4 Lịch Oncall Vip Bệnh viện~~Online
        2	:	1.3 Lịch DS BS trả kết quả~~Online
        3	:	21. PK Ngoại Tim mạch.xlsx
        4	:	1.1 Lịch trực Bệnh viện>TRỰC~~Online
        5	:	1.1 Lịch trực Bệnh viện>LỊCH TRỰC CODE BLUE~~Online
        6	:	1.1 Lịch trực Bệnh viện>HỘI CHẨN~~Online
        7	:	1.2 Lịch Cận lâm sàng
        8	:	1.5. Lịch khám oncall các Chuyên khoa Khu tiêu chuẩn
 """

    # st.table(ten_PK_theo_KHTH)

    ten_PK_theo_KHTH_dict = []
    # for each row, get row 1 as key and from row 2 is value of ten_PK_theo_KHTH_dict
    for i in range(0, len(ten_PK_theo_KHTH)):
        # add to dictionary ten_PK_theo_KHTH_dict ten_PK_theo_KHTH.iloc[0].to_dict()
        ten_PK_theo_KHTH_dict.append(ten_PK_theo_KHTH.iloc[i].to_dict())

    # st.write(ten_PK_theo_KHTH_dict)
    # st.write(ten_PK_theo_KHTH)

    # # loop through all ten_PK_theo_KHTH_dict
    # for i in range(0, len(ten_PK_theo_KHTH_dict)-1):
    #     st.write(ten_PK_theo_KHTH_dict[i])

    st.session_state.ten_PK_theo_KHTH_dict = ten_PK_theo_KHTH_dict
    # print(ten_PK_theo_KHTH_dict)
    return ten_PK_theo_KHTH_dict
