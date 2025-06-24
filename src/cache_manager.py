from datetime import datetime
import streamlit as st

def manage_cache():
    if 'last_interaction' not in st.session_state:
        st.session_state.last_interaction = datetime.now()

    MAX_INACTIVITY_DURATION = 30*60 # Define inactivity time 30 min of inactivity
    current_time = datetime.now()
    inactivity_duration = (current_time - st.session_state.last_interaction).seconds

    if inactivity_duration > MAX_INACTIVITY_DURATION:
        st.warning("The session was close due to inactivity")
        if st.session_state.logged_in:
            st.session_state.logged_in = False
            st.session_state.expired = True
            st.rerun()
    else:
        st.session_state.last_interaction = datetime.now()
