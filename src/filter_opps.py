import numpy as np
import streamlit as st
from dateutil.relativedelta import relativedelta


def define_filters(data, key_prefix=""):
    period = st.radio("Period", sorted(list(data['Period'].unique()), reverse=True), horizontal=True, label_visibility="collapsed",key=f"{key_prefix}_period")
    filtered_data = data[data['Period'] == period]

    start_date =  np.datetime64(period, 'D')
    end_date = np.datetime64(start_date + relativedelta(months=1))

    # Filter data based on date range
    filtered_data = filtered_data[(filtered_data['ValidFromDate'] >= start_date) & (filtered_data['ValidFromDate'] < end_date)]

    if key_prefix != "tab2":
        type = st.sidebar.selectbox("Opportunity Type", options=['All'] + list(filtered_data['Opportunity Type'].unique()),key=f"{key_prefix}_type")
        if type != 'All':
            filtered_data = filtered_data[filtered_data['Opportunity Type'] == type]

    source = st.sidebar.selectbox("Opportunity Source", options=['All'] + list(filtered_data['Opportunity Source'].unique()),key=f"{key_prefix}_source")
    if source != 'All':
        filtered_data = filtered_data[filtered_data['Opportunity Source'] == source]

    product = st.sidebar.selectbox("Product", options=['All'] + list(filtered_data['Product Family'].unique()),key=f"{key_prefix}_product")
    if product != 'All':
        filtered_data = filtered_data[filtered_data['Product Family'] == product]

    region = st.sidebar.selectbox("Region", options=['All'] + list(filtered_data['Territory Bucket'].unique()),key=f"{key_prefix}_region")
    if region != 'All':
        filtered_data = filtered_data[filtered_data['Territory Bucket'] == region]


    return filtered_data, period

