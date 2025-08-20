import random
import streamlit as st
import func.x0_2_xuat_all_combined_save_to_excel as x0_2_xuat_all_combined_save_to_excel
# LOAD STYLE CSS
from streamlitGUI.s1_style_load import local_css
from SETTINGS_FOR_ALL import SETTINGS

local_css("streamlitGUI/s1_style_load_streamlit.css")
headingcolors = ["#900050", "#003be8", "RGBA(13,202,240,var(--bs-bg-opacity,1))!important", "RGBA(255,193,7,var(--bs-bg-opacity,1))!important"]

st.markdown(f'''
    <style>
            h4,h5 {{background-color: {random.choice(headingcolors)}; padding: 10px !important; border-radius: 5px; margin-bottom:10px !important}}
    </style>
''', unsafe_allow_html=True)

x0_2_xuat_all_combined_save_to_excel.create_excel_file()
st.balloons()

# Function to display data in a given column
def display_data_in_column(column, data_list):
    with column:
        for tenFileDeXuatHienTai in data_list:
            try:
                st.write(f"##### PK: {tenFileDeXuatHienTai}")
                # column_name = name_KHTH of st.session_state.ten_PK_theo_KHTH_dict have file_sheet_name = tenFileDeXuatHienTai
                col_name = SETTINGS["column_name_thongKe"][tenFileDeXuatHienTai]
                
                value_counts = st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"][col_name].value_counts()
                # st.write total row of st.session_state[f"final_sheet_of_{tenFileDeXuatHienTai}"]
                st.write(f"**Tổng số dòng:** {len(st.session_state[f'final_sheet_of_{tenFileDeXuatHienTai}'])}")
                st.write(value_counts)
            except Exception as e:
                st.warning(f"❌ Không có dữ liệu: ***{tenFileDeXuatHienTai}***")

# Split the list into two halves
unique_list = st.session_state.ten_PK_theo_KHTH_unique
mid_index = len(unique_list) // 2
first_half = unique_list[:mid_index]
second_half = unique_list[mid_index:]

# Create two columns
col1, col2 = st.columns(2)

# Display data in each column
display_data_in_column(col1, first_half)
display_data_in_column(col2, second_half)