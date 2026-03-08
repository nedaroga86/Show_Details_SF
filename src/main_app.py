import os

import pandas as pd
import streamlit as st
from glob import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
icon =  os.path.join(BASE_DIR, '..', 'images','logo.ico')


OPPS_DIR = os.path.join(BASE_DIR, '..', 'data', 'opportunities')
LEADS_DIR = os.path.join(BASE_DIR, '..', 'leads', 'opportunities')

file_2025_5 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2025_5.csv')
file_2025_6 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2025_6.csv')
file_2025_7 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2025_7.csv')
file_2025_8 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2025_8.csv')
file_2025_9 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2025_9.csv')
file_2025_10 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2025_10.csv')
file_2025_11 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2025_11.csv')
file_2025_12 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2025_12.csv')
file_2026_1 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2026_1.csv')
file_2026_2 =  os.path.join(BASE_DIR,'..', 'data', 'leads','2026_2.csv')

def load_opp():
    if st.session_state.get('data_loaded', False):
        return st.session_state['opps']

    files = sorted(glob(os.path.join(OPPS_DIR, '*.csv')))

    dfs = []
    for f in files:
        df = pd.read_csv(f, parse_dates=['ValidFromDate', 'ValidToDate'])
        df['Amount'] = df['Amount'].replace({',': ''}, regex=True).astype(float)
        dfs.append(df)


    opps = pd.concat(dfs, ignore_index=True)
    opps.columns = opps.columns.str.strip()

    opps['ValidToDate'] = opps['ValidToDate'].replace('3000-01-01', '2250-01-01')
    opps['ValidToDate'] = pd.to_datetime(opps['ValidToDate'], errors='coerce')

    opps['Amount'] = pd.to_numeric(opps['Amount'], errors='coerce')

    st.session_state['opps'] = opps
    st.session_state['data_loaded'] = True
    return opps


def load_leads_new(): ## Por finalizar
    if st.session_state.get('leads_loaded', False):
        return st.session_state['leads']

    files = sorted(glob(os.path.join(LEADS_DIR, '*.csv')))

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        dfs.append(df)

    opps = pd.concat(dfs, ignore_index=True)


    st.session_state['leads'] = opps
    st.session_state['leads_loaded'] = True
    return st.session_state['leads']

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
        f_2025_9 = pd.read_csv(file_2025_9)
        f_2025_9['Period'] = '2025-09-01'
        f_2025_10 = pd.read_csv(file_2025_10)
        f_2025_10['Period'] = '2025-10-01'
        f_2025_11 = pd.read_csv(file_2025_11)
        f_2025_11['Period'] = '2025-11-01'
        f_2025_12 = pd.read_csv(file_2025_12)
        f_2025_12['Period'] = '2025-12-01'
        f_2026_1 = pd.read_csv(file_2026_1)
        f_2026_1['Period'] = '2026-01-01'
        f_2026_2 = pd.read_csv(file_2026_2)
        f_2026_2['Period'] = '2026-01-02'
        st.session_state['leads'] = pd.concat([f_2025_5, f_2025_6,f_2025_7,f_2025_8,f_2025_9,f_2025_10,f_2025_11,f_2025_12,f_2026_1,f_2026_2])
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
    pages = [
        st.Page("new_pipeline.py", title="New Pipeline"),
        st.Page("opportunity_source.py", title="Opportunity Source"),
        st.Page("priority_leads.py", title="Priority Leads"),
        st.Page("converted_leads.py", title="Converted Leads"),
        st.Page("logout.py", title="Logout")
    ]
    pg = st.navigation(pages, position="top")
    pg.run()

