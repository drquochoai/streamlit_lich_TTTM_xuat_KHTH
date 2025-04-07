import streamlit as st
from streamlit.runtime.scriptrunner import RerunData, RerunException


def clear_cache_rerun():

    # Clear all caches
    st.cache_data.clear()
    st.cache_resource.clear()
    
    # Force a rerun
    RerunException(RerunData())
