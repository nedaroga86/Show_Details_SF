import streamlit as st
from tables_leads import show_leads_table

def show_priority_leads():

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
    periods = sorted(leads_df['Period'].unique().tolist(), reverse=True)
    period = st.radio("Period", periods, horizontal=True, label_visibility="collapsed")

    leads_df = leads_df[leads_df['Period'] == period]

    st.subheader("Lead Priority Details", divider="red")
    show_leads_table(leads_df,period)

show_priority_leads()