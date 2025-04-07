import streamlit as st
import pandas as pd
from func.o1_help_ten_PK_theo_KHTH import xuLyTenDanhSachPK
from func.x1_xuat_phong_kham_Noi_Ngoai_TM import xuatPhongKham
from SETTINGS_FOR_ALL import SETTINGS

st.set_page_config(
    page_title="Xuất file lịch TTTM",
    page_icon="👋",
)


# LOAD STYLE CSS
from streamlitGUI.s1_style_load import local_css
local_css("streamlitGUI/s1_style_load_streamlit.css")

from func.a1_0_load_url_theo_demo import load_url_theo_demo
url = load_url_theo_demo()

# $ TẢI FILE EXCEL VỀ MÁY
from func.a1_1_load_excel_from_url import load_excel_data_from_url
st.session_state.full_lich = load_excel_data_from_url(url)


# HIỂN THỊ MENU CÁCH XUẤT FILE LỊCH TTTM
# ten_PK_theo_KHTH = get sheet "🏥Tên PK theo KHTH" from the full_lich
# st.write(full_lich)
xuLyTenDanhSachPK(st.session_state.full_lich)


# xuatPhongKham(st.session_state.full_lich, "Tháng 5-2025")

# CÓ FILE EXCEL RỒI, BÂY GIỜ hiển thị các sheet names trong file excel dạng dropdown
# st.write(st.session_state)
from streamlitGUI.p1_load_sheetNames_of_excel_gui import load_sheet_names_of_excel
load_sheet_names_of_excel()

# load trang chủ streamlit
from streamlitGUI.o1_0_homepage_gui import trangchu
trangchu()
