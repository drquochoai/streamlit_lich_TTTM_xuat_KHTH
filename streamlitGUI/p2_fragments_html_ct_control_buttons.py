import html
import streamlit as st
from SETTINGS_FOR_ALL import SETTINGS
from datetime import datetime


@st.fragment
def ct_control_buttons_html_string(b64):
    # Create a container for control buttons
    # create st download_button  excel file with b64 data
    # get current date time for the name of file
    # Get the current date and time
    current_datetime = datetime.now().strftime("%d.%m.%Y lúc %Hh%Mm%S")
    name_of_file = SETTINGS["name_of_exported_file"] + " - "+ st.session_state.selected_sheet_name + " - "+ current_datetime + ".xlsx"
    html_string = f'''
    <a href = "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download = "{name_of_file}"
    class="button-5 dr-tai-excel-automatic"> 
        TẢI FILE EXCEL
    </a>
    '''
    
    return html_string