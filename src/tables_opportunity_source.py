import os

import numpy as np
import pandas as pd
import streamlit as st

from logout import call_logout
from filter_opps import define_filters

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
opportunity_source_file = os.path.join(BASE_DIR, '..', 'data', 'Opportunities.csv')



def show_opportunity_source_table():
    st.title('Opportunity Source Table')

    st.session_state['opps_filtered'],st.session_state['period'] = define_filters(st.session_state['opps'])

    filtered_data = st.session_state['opps_filtered']

    filtered_data = filtered_data[filtered_data['Opportunity Type']== 'New Customer']

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
    st.text(f"Opportunities for {st.session_state['period']}: {filtered_data['Amount'].sum()/1000:,.0f}K")
    filtered_data.rename(columns={
        'Opportunity.Created Date': 'Created Dates',
        'Opportunity.Close Date': 'Close Dates'
    }, inplace=True)

    filtered_data = filtered_data.sort_values(by='Amount', ascending=False)
    filtered_data['Amount'] = (filtered_data['Amount']/1000).astype('int').round(0)
    st.dataframe(filtered_data[['Opportunity ID', 'Opportunity Number', 'Stage Name', 'Name', 'Stage', 'Created Dates','Close Dates','Amount']], use_container_width =True, hide_index=True, height=700)

show_opportunity_source_table()