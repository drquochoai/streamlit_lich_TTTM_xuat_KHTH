from numpy import add
import streamlit as st
from SETTINGS_FOR_ALL import SETTINGS
from func.x0_1_xuat_all_combined import xuat_all_combined

from streamlitGUI.s1_style_load import add_click_button
from func.u1_utils_clear_CACHE_RERUN import clear_cache_rerun


def load_sheet_names_of_excel():
    """
    """
    # sheet_names_only = JUST GET SHEET NAMES in st.session_state.sheet_names START WITH "Tháng" to show in dropdown
    # and not contain "$" in name
    col1, col2, col3 = st.columns(3)
    with col1:
        add_click_button(SETTINGS['url']['edit'], "Edit file lịch")
    with col2:
        add_click_button(SETTINGS['url']['downloadFull'], "Tải file")
    with col3:
        st.button("🔄 RELOAD EXCEL", on_click=lambda: clear_cache_rerun(),
                  type="primary")

    sheet_names_only = []
    if "sheet_names" in st.session_state:
        # st.write(st.session_state)
        for name in st.session_state.sheet_names:
            if name.lower().startswith("tháng") and "$" not in name.lower():
                sheet_names_only.append(name)       
    else: 
        clear_cache_rerun()

    # sheet_names_only = [name for name in st.session_state.sheet_names if name.lower().startswith("tháng") or name.lower().startswith("template")]
    # st.write(sheet_names_only)
    # dropdown select with searchable : st.session_state.sheet_names
    # Create searchable dropdown for selecting a sheet

    st.write("# Chọn các mục cần xuất")
    # Create a form for file export options
    with st.form(key='form_export_file_KHTH'):
        st.selectbox(
            "Chọn sheet cần xuất",
            options=sheet_names_only,
            index=0,
            key="selected_sheet"
        )
        st.session_state.selected_sheet_name = st.session_state.selected_sheet
        # create 3 columns
        col1, col2, col3 = st.columns(3)
        # st.write(st.session_state.ten_PK_theo_KHTH_unique)
        # Split the list into chunks of 4 items each
        chunk_size = 3
        ten_PK_chunks= []
        if "ten_PK_theo_KHTH_unique" in st.session_state:
            ten_PK_chunks = [st.session_state.ten_PK_theo_KHTH_unique[i:i + chunk_size]
                            for i in range(0, len(st.session_state.ten_PK_theo_KHTH_unique), chunk_size)]
        else:
            clear_cache_rerun()
        # Distribute chunks to columns
        if len(ten_PK_chunks) == 0:
            st.warning("Không có phòng khám nào để xuất")
            clear_cache_rerun()
            return
        for i, chunk in enumerate(ten_PK_chunks):
            target_col = [col1, col2, col3][i % 3]  # Rotates through columns
            with target_col:
                for ten_PK in chunk:
                    st.checkbox(ten_PK, value=True, key=f"cb_export_{ten_PK}")
        # Submit button to process the form
        submit_button = st.form_submit_button(label="Xuất file")
        # st.write(st.session_state)
        if submit_button:
            # st.write(st.session_state.cb_export_lich_PK)
            st.spinner("Đang xuất file...")
            # run function to export file
            xuat_all_combined()
            """
            This container is used to display the status of the export process.
            It will show a message when the export is complete.
            """
