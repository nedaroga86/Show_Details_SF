import os

import numpy as np
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
opportunities_file =  os.path.join(BASE_DIR,'..', 'data', 'May_2025.csv')




def load_data():
    if not st.session_state.get('data_loaded', False):
        st.session_state['opps'] = pd.read_csv(opportunities_file)
        st.session_state['opps'].columns = st.session_state['opps'].columns.str.strip()
        st.session_state['opps']['ValidFromDate'] = st.session_state['opps']['ValidFromDate'].astype('datetime64[ns]')
        st.session_state['opps']['ValidToDate'] = np.where(st.session_state['opps']['ValidToDate'] == '3000-01-01', '2250-01-01', st.session_state['opps']['ValidToDate'])
        st.session_state['opps']['ValidToDate'] = st.session_state['opps']['ValidToDate'].astype('datetime64[ns]')
        st.session_state['opps']['Amount'] = pd.to_numeric(st.session_state['opps']['Amount'], errors='coerce')

        st.session_state['data_loaded'] = True

    return st.session_state['opps']


def get_data():
    if 'opps' not in st.session_state:
        st.session_state['opps'] = load_data()
    return st.session_state['opps']

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




def show_opportunity_table():

    st.subheader('Opportunities Table')
    data = get_data()
    start_date =  np.datetime64('2025-05-01', 'D')
    end_date = np.datetime64('2025-05-31', 'D')

    # Filter data based on date range
    filtered_data = data[(data['ValidFromDate'] >= start_date) & (data['ValidFromDate'] <= end_date)]

    # fILTER LOST REASON NOT DUPLICATE
    # st.text(filtered_data.columns)
    product = st.sidebar.selectbox("Product", options=['All'] + list(filtered_data['Product Family'].unique()), key='product_family')
    if product != 'All':
        filtered_data = filtered_data[filtered_data['Product Family'] == product]

    region = st.sidebar.selectbox("Region", options=['All'] + list(filtered_data['Territory Bucket'].unique()), key='territory_bucket')
    if region != 'All':
        filtered_data = filtered_data[filtered_data['Territory Bucket'] == region]

    filtered_data = filtered_data[~filtered_data['Loss Reason'].isin(['Duplicate', 'Duplicate Opportunity'])]

    filtered_data['first_day_of_month'] = filtered_data['ValidFromDate'].dt.to_period('M').dt.to_timestamp()
    filtered_data['Last_day_of_month'] = filtered_data['ValidToDate'].dt.to_period('M').dt.to_timestamp()
    filtered_data['is_valid'] = filtered_data['Last_day_of_month'] > filtered_data['first_day_of_month']




    target_date = pd.to_datetime("1899-12-30") + pd.to_timedelta(32874, unit="D")

    filtered_data['Prev Close Date'] = pd.to_datetime(filtered_data['Prev Close Date'], errors='coerce')
    mask = filtered_data['Prev Close Date'] == target_date

    min_valid_from = (
        filtered_data[mask]
        .groupby('Opportunity ID')['first_day_of_month']
        .min()
        .rename('min_valid_from')
    )
    filtered_data = filtered_data.merge(min_valid_from, on='Opportunity ID', how='left')
    filtered_data['is_earliest'] = filtered_data['first_day_of_month'] == filtered_data['min_valid_from']
    filtered_data = filtered_data[(filtered_data['is_valid'])&(filtered_data['is_earliest'])]


    filtered_data = filtered_data[~((filtered_data['Product Family'] == 'ZTNA') & (filtered_data['Subtype'] == 'Usage Based'))]

    # Display the table
    st.text(f"Opportunities for May 2025: {filtered_data['Amount'].sum()/1000:,.0f}K")
    filtered_data.rename(columns={
        'Opportunity.Created Date': 'Created Dates',
        'Opportunity.Close Date': 'Close Dates'
    }, inplace=True)

    filtered_data = filtered_data.sort_values(by='Amount', ascending=False)
    filtered_data['Amount'] = (filtered_data['Amount']/1000).astype('int').round(0)
    st.dataframe(filtered_data[['Opportunity ID', 'Opportunity Number', 'Stage Name', 'Name', 'Stage', 'Created Dates','Close Dates','Amount']], use_container_width =True, hide_index=True, height=700)


show_opportunity_table()