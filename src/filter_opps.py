import numpy as np
import streamlit as st
from dateutil.relativedelta import relativedelta


def define_filters(data):
    period = st.sidebar.selectbox("Period", list(data['Period'].unique()))
    filtered_data = data[data['Period'] == period]


    start_date =  np.datetime64(period, 'D')
    end_date = np.datetime64(start_date + relativedelta(months=1))

    # Filter data based on date range
    filtered_data = filtered_data[(filtered_data['ValidFromDate'] >= start_date) & (filtered_data['ValidFromDate'] <= end_date)]

    product = st.sidebar.selectbox("Product", options=['All'] + list(filtered_data['Product Family'].unique()))
    if product != 'All':
        filtered_data = filtered_data[filtered_data['Product Family'] == product]

    region = st.sidebar.selectbox("Region", options=['All'] + list(filtered_data['Territory Bucket'].unique()))
    if region != 'All':
        filtered_data = filtered_data[filtered_data['Territory Bucket'] == region]


    return filtered_data, period