import os

import numpy as np
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
opportunities_file =  os.path.join(BASE_DIR,'..', 'data', 'Clean_leads.csv')




def load_data():
    if not st.session_state.get('leads_loaded', False):
        st.session_state['leads'] = pd.read_csv(opportunities_file)
        st.session_state['leads_loaded'] = True
    return st.session_state['leads']


def get_data():
    if 'leads' not in st.session_state:
        st.session_state['leads'] = load_data()
    return st.session_state['leads']

def get_open_Stage():
    data = get_data()
    open_stages = data['Stage Name'].unique().tolist()
    open_stages = [stage for stage in open_stages if stage not in ['100% Signed Agreement', '0% Closed Lost']]
    return open_stages

def get_all_Stages():
    data = get_data()
    all_stages = data['Stage Name'].unique().tolist()
    all_stages = [stage for stage in all_stages if stage not in ['100% Signed Agreement', '0% Closed Lost']]
    all_stages.append('100% Signed Agreement')
    all_stages.append('0% Closed Lost')
    return all_stages




def show_leads_table():
    st.subheader('Leads Table')
    leads_df = get_data()
    start_date =  np.datetime64('2025-05-01', 'D')
    end_date = np.datetime64('2025-05-31', 'D')

    list_priority = ['Priority 1', 'Priority 2', 'Priority 3']

    lead_priority = st.sidebar.radio("Lead Priority", options=['All'] + list_priority, key='Lead_Priority')
    if lead_priority != 'All':
        filtered_df = leads_df[leads_df['Lead Priority'] == lead_priority]
    else:
        filtered_df = leads_df


    mask = (
            (filtered_df['Special Exclusion'].isna()) &
            (pd.to_datetime(filtered_df['RFS Date/Time']) >= start_date) &
            (pd.to_datetime(filtered_df['RFS Date/Time']) < end_date) &
            (filtered_df['Marketing Source'] == 1) &
            (filtered_df['Name'] == 'Sales Generated Lead') &
            (filtered_df['Territory Bucket'].notna()) &
            (filtered_df['Territory Bucket'] != '') &
            (filtered_df['Territory Bucket'] != 'Non-RSD Total') &
            filtered_df['Priotity Exclusion'].isna()
    )

    st.text(f"Number of leads: {filtered_df[mask].shape[0]}")
    st.dataframe(filtered_df[mask], use_container_width=True, height=700)

show_leads_table()