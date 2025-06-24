import os
import streamlit as st


def set_config_page():

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        logo = os.path.join(BASE_DIR, '..', 'images', "logo.png")
        st.logo(logo)
    except:
        pass
    st.layout="wide"