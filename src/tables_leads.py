
import numpy as np
import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta

from main_app import get_data



def show_leads_table(leads_df, period):
    if 'leads' not in st.session_state:
        get_data()
    start_date =  np.datetime64(period, 'D')
    end_date = np.datetime64(start_date + relativedelta(months=1))
    st.text(start_date)
    st.text(end_date)

    list_priority = ['Priority 1', 'Priority 2', 'Priority 3']
    lead_priority = st.sidebar.radio("Lead Priority", options=['All'] + list_priority, key='Lead_Priority')
    if lead_priority != 'All':
        filtered_df = leads_df[leads_df['Lead Priority'] == lead_priority]
    else:
        filtered_df = leads_df

    st.dataframe(filtered_df, use_container_width=True, height=800)

    priority_mask = (
            (filtered_df['Special Exclusion'].isna()) &
            (pd.to_datetime(filtered_df['RFS Date/Time']) >= start_date) &
            (pd.to_datetime(filtered_df['RFS Date/Time']) < end_date) &
            # (filtered_df['Marketing Source'] == 1) &
            # (filtered_df['Name'] == 'Sales Generated Lead') &
            # (filtered_df['Territory Bucket'].notna()) &
            # (filtered_df['Territory Bucket'] != '') &
            # (filtered_df['Territory Bucket'] != 'Non-RSD Total') &
            filtered_df['Priotity Exclusion'].isna()
    )


    st.text(f"Number of leads: {filtered_df[priority_mask].shape[0]}")
    st.dataframe(filtered_df[priority_mask], use_container_width=True, height=800)

