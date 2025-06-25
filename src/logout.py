import streamlit as st
import os
def call_logout():
    st.set_page_config(initial_sidebar_state="collapsed")
    st.session_state.clear()
    # Redirect to the login page
    st.session_state.logged_in = False
    st.rerun()

