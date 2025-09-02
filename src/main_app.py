import os
import numpy as np
import pandas as pd
import streamlit as st
from logout import call_logout

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
icon =  os.path.join(BASE_DIR, '..', 'images','logo.ico')


opportunities_file_2025_3 =  os.path.join(BASE_DIR,'..', 'data', 'opportunities','opportunities_2025-03-01.csv')
opportunities_file_2025_4 =  os.path.join(BASE_DIR,'..', 'data', 'opportunities','opportunities_2025-04-01.csv')
opportunities_file_2025_5 =  os.path.join(BASE_DIR,'..', 'data', 'opportunities', 'opportunities_2025-05-01.csv')
opportunities_file_2025_6 =  os.path.join(BASE_DIR,'..', 'data', 'opportunities', 'opportunities_2025-06-01.csv')
opportunities_file_2025_7 =  os.path.join(BASE_DIR,'..', 'data', 'opportunities', 'opportunities_2025-07-01.csv')
opportunities_file_2025_8 =  os.path.join(BASE_DIR,'..', 'data', 'opportunities', 'opportunities_2025-08-01.csv')

file_2025_5 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2025_5.csv')
file_2025_6 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2025_6.csv')
file_2025_7 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2025_7.csv')
file_2025_8 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2025_8.csv')


def load_opp():
    if not st.session_state.get('data_loaded', False):
        st.session_state['opps'] = pd.concat([
            pd.read_csv(opportunities_file_2025_3),
            pd.read_csv(opportunities_file_2025_4),
            pd.read_csv(opportunities_file_2025_5),
            pd.read_csv(opportunities_file_2025_6),
            pd.read_csv(opportunities_file_2025_7),
            pd.read_csv(opportunities_file_2025_8)
        ], ignore_index=True)

        st.session_state['opps'].columns = st.session_state['opps'].columns.str.strip()
        st.session_state['opps']['ValidFromDate'] = st.session_state['opps']['ValidFromDate'].astype('datetime64[ns]')
        st.session_state['opps']['ValidToDate'] = np.where(st.session_state['opps']['ValidToDate'] == '3000-01-01', '2250-01-01', st.session_state['opps']['ValidToDate'])
        st.session_state['opps']['ValidToDate'] = st.session_state['opps']['ValidToDate'].astype('datetime64[ns]')
        st.session_state['opps']['Amount'] = pd.to_numeric(st.session_state['opps']['Amount'], errors='coerce')
        st.session_state['data_loaded'] = True
    return st.session_state['opps']

def load_leads():
    if not st.session_state.get('leads_loaded', False):
        f_2025_5 = pd.read_csv(file_2025_5)
        f_2025_5['Period'] = '2025-05-01'
        f_2025_6 = pd.read_csv(file_2025_6)
        f_2025_6['Period'] = '2025-06-01'
        f_2025_7 = pd.read_csv(file_2025_7)
        f_2025_7['Period'] = '2025-07-01'
        f_2025_8 = pd.read_csv(file_2025_8)
        f_2025_8['Period'] = '2025-08-01'
        st.session_state['leads'] = pd.concat([f_2025_5, f_2025_6,f_2025_7,f_2025_8])
        st.session_state['leads_loaded'] = True
    return st.session_state['leads']


def get_data():
    if 'opps' not in st.session_state:
        st.session_state['opps'] = load_opp()
        st.session_state['leads'] = load_leads()
    return st.session_state['opps'],st.session_state['leads']



def call_main_app():


    with st.spinner("Wait for it..."):
        get_data()
    logout = st.sidebar.button('Logout', key='logout_button',type='primary')
    if logout:
        call_logout()


    pages = {
        "Opportunities": [
            st.Page("tables_opportunities.py", title="New Pipeline"),
            st.Page("tables_opportunity_source.py", title="Opportunities Source"),
        ],
        "Leads": [
            st.Page("tables_leads.py", title="Priority Leads"),
            st.Page("tables_converted_leads.py", title="Converted Leads"),
        ]
    }


    pg = st.navigation(pages, position="top")
    pg.run()
