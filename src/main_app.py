import os

import numpy as np
import pandas as pd
import streamlit as st

from filter_opps import define_filters

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
icon =  os.path.join(BASE_DIR, '..', 'images','logo.ico')


opportunity_source_file = os.path.join(BASE_DIR, '..', 'data', 'Opportunities.csv')

def load_opp():
    if not st.session_state.get('data_loaded', False):
        st.session_state['opps'] = pd.read_csv(opportunity_source_file)
        st.session_state['opps'].columns = st.session_state['opps'].columns.str.strip()
        st.session_state['opps']['ValidFromDate'] = st.session_state['opps']['ValidFromDate'].astype('datetime64[ns]')
        st.session_state['opps']['ValidToDate'] = np.where(st.session_state['opps']['ValidToDate'] == '3000-01-01', '2250-01-01', st.session_state['opps']['ValidToDate'])
        st.session_state['opps']['ValidToDate'] = st.session_state['opps']['ValidToDate'].astype('datetime64[ns]')
        st.session_state['opps']['Amount'] = pd.to_numeric(st.session_state['opps']['Amount'], errors='coerce')
        st.session_state['data_loaded'] = True
    return st.session_state['opps']

def get_data():
    if 'opps' not in st.session_state:
        st.session_state['opps'] = load_opp()
    return st.session_state['opps']



def call_main_app():

    st.set_page_config(page_title="Details Table Analysis", layout='wide', page_icon=icon, initial_sidebar_state="expanded")
    get_data()
    st.session_state['opps_filtered'],st.session_state['period'] = define_filters(st.session_state['opps'])

    pages = {
        "Opportunities": [
            st.Page("tables_opportunities.py", title="New Pipeline"),
            st.Page("tables_opportunity_source.py", title="Opportunities Source"),
        ],
        "Leads": [
            st.Page("tables_leads.py", title="Priority Leads"),
            st.Page("tables_converted_leads.py", title="Converted Leads"),
        ],
    }


    pg = st.navigation(pages, position="top")
    pg.run()



call_main_app()