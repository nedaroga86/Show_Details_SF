import streamlit as st
def call_logout():
    st.session_state.logged_in = False
    for k in list(st.session_state.keys()):
        if k not in ["logger"]:  # si tienes logger persistente
            del st.session_state[k]

    # 🔄 Recarga la app base (esto desmonta el menú visual)
    st.markdown(
        "<meta http-equiv='refresh' content='0; url=/'/>",
        unsafe_allow_html=True,
    )

call_logout()