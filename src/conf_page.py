import os
import streamlit as st


def set_config_page():
    st.markdown(
        """
        <style>
        /* Hide the Streamlit header and hamburger menu */
        header, footer, .css-18e3th9 {
            visibility: hidden;
            height: 10px;
            margin: 0;
            padding: 0;
        }
    
        /* Optional: Further reduce top padding if needed */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.session_state.theme = "light"
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        logo = os.path.join(BASE_DIR, '..', 'images', "logo.png")
        st.logo(logo)
    except:
        pass
    st.layout="wide"