import streamlit as st

from tables_converted_leads import show_converted_table


def show_converted_leads():

    st.markdown("""
        <style>
        /* Reduce padding superior de toda la app */
        .block-container {
            padding-top: 3rem;
            padding-bottom: 0rem;
        }
        </style>
    """, unsafe_allow_html=True)

    leads_df = st.session_state.leads.copy()
    periods = leads_df['Period'].unique().tolist()
    period = st.radio("Period", periods, horizontal=True, label_visibility="collapsed")

    leads_df = leads_df[leads_df['Period'] == period]

    st.subheader("Lead Details", divider="red")
    show_converted_table(leads_df, period)


show_converted_leads()