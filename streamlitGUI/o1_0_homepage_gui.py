import streamlit as st
from SETTINGS_FOR_ALL import SETTINGS
import streamlitGUI.s1_style_load as style_load
def trangchu():
    if st.session_state.workingWithDemo:
        st.write("# Xuất file tự động! 👋")
        st.session_state.workingWithDemo = SETTINGS['workingWithDemo']
        
        st.write("### Đang chạy demo, hãy sửa SETTINGS['workingWithDemo'] thành False nếu muốn chạy thật...")
        # add 4 column
        col1, col2 = st.columns(2)
        # add button to col1: name xemFileDemo, url = SETTINGS['url']['editDemo']
        with col1:
            # add button to col1: name xemFileDemo, open url = SETTINGS['url']['editDemo'] without reload the page
            style_load.add_click_button(SETTINGS['url']['edit'], "Edit file lịch")
            if st.session_state.workingWithDemo:
                # add button to col1: name xemFileDemo, open url = SETTINGS['url']['editDemo'] without reload the page
                style_load.add_click_button(SETTINGS['url']['editDemo'], "Edit file Demo")
        with col2:
            # add button to col2: name xemFileFull, url = SETTINGS['url']['edit']
            style_load.add_click_button(SETTINGS['url']['downloadFull'], "Tải file Lịch", style="button-22")
            if st.session_state.workingWithDemo:
                # add button to col2: name xemFileFull, url = SETTINGS['url']['edit']
                style_load.add_click_button(SETTINGS['url']['downloadDemo'], "Tải file Demo", style="button-22")
        # add button to col2: name xemFileFull, url = SETTINGS['url']['edit']
        
        # add a div to show the status of the button
    
if __name__ == "__main__":
    trangchu()
