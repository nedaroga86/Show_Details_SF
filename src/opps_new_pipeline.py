import pandas as pd
import streamlit as st



def show_opportunity_table(filtered_data):

    filtered_data.rename(columns={
        'Opportunity.Created Date': 'Created Dates',
        'Opportunity.Close Date': 'Close Dates'
    }, inplace=True)

    filtered_data = filtered_data.sort_values(by='Amount', ascending=False)
    filtered_data['Amount'] = (filtered_data['Amount']/1000).astype('int').round(2)
    num_rows = len(filtered_data)
    height = min(800, max(300, num_rows * 25))
    st.dataframe(filtered_data[['Opportunity ID', 'Opportunity Number', 'Account Name','Stage Name', 'Name', 'Stage', 'Created Dates','Full Name',
                                'Close Dates','Amount','Product Family','Industry','Territory Bucket','Market Segment','Opportunity Type']],
                 use_container_width =True, hide_index=True, height=height)


def preprocess_data(filtered_data):

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
    filtered_data = filtered_data[(filtered_data['is_valid']) & (filtered_data['is_earliest'])]

    filtered_data = filtered_data[
        ~((filtered_data['Product Family'] == 'ZTNA') & (filtered_data['Subtype'] == 'Usage Based'))]
    return filtered_data
