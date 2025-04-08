import pandas as pd
import streamlit as st
import tempfile
import os
import base64
from streamlit.components.v1 import html
import streamlitGUI.p2_fragments_html_ct_control_buttons as ct_control_buttons

def create_excel_file():
    """Create and automatically download an Excel file from session state data"""
    prefix_name = "final_sheet_of_"
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            temp_file_path = tmp.name

        # Create a dictionary to store all dataframes that match our criteria
        sheets_to_export = {}

        # Find all relevant dataframes in session state
        for key in st.session_state.keys():
            if str(key).startswith(prefix_name):
                sheets_to_export[key] = st.session_state[key]

        # Only proceed if we found any data to export
        if not sheets_to_export:
            ct_control_buttons.ct_control_buttons_html_string("ll")
            st.warning(
                "No data found to export - no data have been loaded 'final_sheet_of_'")

            # navigate to home page
            st.switch_page("💘Xuất Lịch TTTM.py")
            return

        # Sort the sheets_to_export dictionary by keys (sheet names)
        sorted_sheets_to_export = dict(sorted(sheets_to_export.items()))

        # Create Excel file
        with pd.ExcelWriter(temp_file_path, engine='openpyxl') as writer:
            for sheet_name, df in sorted_sheets_to_export.items():
                # Ensure we're working with a DataFrame
                if not isinstance(df, pd.DataFrame):
                    st.warning(
                        f"Key '{sheet_name}' doesn't contain a DataFrame, skipping")
                    continue

                # Write to excel file (sheet names max 31 chars)

                sheet_name = sheet_name[len(prefix_name):]  # Remove prefix
                sheet_name = sheet_name.replace("Lịch trực Bệnh viện", "Trực BV")
                sheet_name = sheet_name.replace("Lịch khám oncall các Chuyên khoa Khu tiêu chuẩn", "Khám oncall tiêu chuẩn")
                sheet_name = sheet_name[:31]  # Truncate to 31 characters
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                # distribute columns width to fit all data in the sheet
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

        # download this excel file pd.ExcelWriter(temp_file_path, engine='openpyxl') as writer automatically
        # create html link to download the file pd.ExcelWriter(temp_file_path, engine='openpyxl') as writer automatically
        with open(temp_file_path, 'rb') as f:
            file_bytes = f.read()
            b64 = base64.b64encode(file_bytes).decode()
            href = f'''
            {ct_control_buttons.ct_control_buttons_html_string(b64)}
            <script type="text/javascript">
                setTimeout(function() {{
                    //document.getElementById("dr-tai-excel").click();
                    document.getElementsByClassName("dr-tai-excel-automatic")[0].click();
                    //document.getElementById("div-dr-tai-excel").remove();
                }}, 10);
            </script>
            '''
            # Auto download TẢI FILE EXCEL this files
            html(href, height=0, width=0)


            # st.markdown(href+clickbtn, unsafe_allow_html=True)
            st.markdown(ct_control_buttons.ct_control_buttons_html_string(b64), unsafe_allow_html=True)
        # Clean up the temporary file
        os.unlink(temp_file_path)

    except Exception as e:
        st.error(f"Error creating Excel file: {str(e)}")
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)