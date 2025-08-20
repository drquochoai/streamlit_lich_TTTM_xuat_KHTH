import random
import streamlit as st
from streamlit.runtime.scriptrunner import RerunData, RerunException


def clear_cache_rerun():
    # key = random.randint(1, 1000)
    # st.button("RELOAD EXCEL", on_click=lambda: clear_cache_rerun(),
    #             type="primary", icon=":material/frame_reload:", key=f'reload_{key}')

    # Clear all caches
    st.cache_data.clear()
    st.cache_resource.clear()
    
    # Force a rerun
    RerunException(RerunData())
