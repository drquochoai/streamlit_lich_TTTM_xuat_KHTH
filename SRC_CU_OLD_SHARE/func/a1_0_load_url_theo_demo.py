from SETTINGS_FOR_ALL import SETTINGS
import streamlit as st

def load_url_theo_demo():
    """
    Determines and returns the appropriate download URL based on the application's demo mode status.
    This function checks the Streamlit session state to determine if the application
    is running in demo mode ('workingWithDemo'). Based on this status, it returns
    either the demo URL or the full version URL from the SETTINGS configuration.
    If 'workingWithDemo' is not set in the session state, it will be initialized to False.
    Returns:
        str: The URL for downloading either the demo version or the full version of the data
    Dependencies:
        - Streamlit (st) for session state management
        - SETTINGS dictionary containing URL configurations
    """

    if st.session_state.get("workingWithDemo") is None:
        st.session_state.workingWithDemo = SETTINGS['workingWithDemo'] # Default to False if not set
    if st.session_state.workingWithDemo:
        url = SETTINGS.get("url", {}).get("downloadDemo") # Demo DEV 💥🏡🏡Lịch làm việc Trung Tâm Tim Mạch
        st.toast("Tải file Demo...")
    else:
        url = SETTINGS.get("url", {}).get("downloadFull")
        st.toast("...💥🏡🏡Lịch TTTM...")
    st.session_state.url = url
    return url

