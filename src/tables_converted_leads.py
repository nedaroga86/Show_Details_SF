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




def show_converted_leads():
    st.subheader('Marketing Leads Converted to Opportunities Total ACV  ')
    leads_df = get_data()
    start_date =  np.datetime64('2025-05-01', 'D')
    end_date = np.datetime64('2025-06-01', 'D')



    mask = (
            (leads_df['Special Exclusion'].isna()) &
            (pd.to_datetime(leads_df['Converted Date']) >= start_date) &
            (pd.to_datetime(leads_df['Converted Date']) < end_date) &
            (leads_df['Marketing Source'] == 1) &
            (leads_df['Name'] == 'Sales Generated Lead') &
            (leads_df['Territory Bucket'].notna()) &
            (leads_df['Territory Bucket'] != '') &
            (leads_df['Territory Bucket'] != 'Non-RSD Total') &
            (leads_df['Lead Status'] == 'Converted') &
            (leads_df['Opportunity ID'].notna())

    )

    st.text(f"Marketing Leads Converted: {leads_df[mask]['Counting Dup Opps'].sum():,.0f} Leads,  {leads_df[mask]['Share Amount'].sum():,.0f} Converted Amount")
    st.dataframe(leads_df[mask][['Lead ID','Lead Source', 'AccountId.Name','Share Amount','Opportunity ID',	'Name.1',	'OwnerId.Name',	'Opportunity Type',	'Opportunity Source',
                                 'Product Family',	'Opportunity.Created Date',	'Opportunity.Close Date']], use_container_width=True, height=700)

