
import streamlit as st
from tables_converted_leads import show_converted_leads
from tables_leads import show_leads_table


leads_df = st.session_state.leads.copy()
periods = leads_df['Period'].unique().tolist()
period = st.radio("Period", periods, horizontal=True, label_visibility="collapsed")

leads_df = leads_df[leads_df['Period'] == period]
lead1, lead2 = st.tabs(["📊 Priority Leads", "📈 Converted Leads"])
with lead1:
    show_leads_table(leads_df,period)
with lead2:
    show_converted_leads(leads_df)