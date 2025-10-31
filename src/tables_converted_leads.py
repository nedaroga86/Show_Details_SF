import numpy as np
import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta

from main_app import get_data



def show_converted_table(leads_df,period):
    if 'leads' not in st.session_state:
        get_data()

    start_date_2 =  np.datetime64(period, 'D')
    end_date_2 = np.datetime64(start_date_2 + relativedelta(months=1))



    mask = (
            (leads_df['Special Exclusion'].isna()) &
            (pd.to_datetime(leads_df['Converted Date']) >= start_date_2) &
            (pd.to_datetime(leads_df['Converted Date']) < end_date_2) &
            (leads_df['Marketing Source'] == 1) &
            (leads_df['Name'] == 'Sales Generated Lead') &
            (leads_df['Territory Bucket'].notna()) &
            (leads_df['Territory Bucket'] != '') &
            (leads_df['Territory Bucket'] != 'Non-RSD Total') &
            (leads_df['Lead Status'] == 'Converted') &
            (leads_df['Opportunity ID'].notna())

    )

    st.text(f"Marketing Leads Converted: {leads_df[mask]['Counting Dup Opps'].sum():,.0f} Leads,  {leads_df[mask]['Amount'].sum():,.0f} Converted Amount")
    opp_converted = leads_df[mask][['Opportunity ID',	'Name.1',	'OwnerId.Name',	'Opportunity Type',	'Opportunity Source','AccountId.Name',
                                    'Product Family', 'Converted Date',	'Opportunity.Created Date',	'Opportunity.Close Date', 'Amount']]
    opp_converted = opp_converted.drop_duplicates()
    height=38+len(opp_converted)*35

    st.dataframe(opp_converted.drop_duplicates().sort_values(by='Amount', ascending=False), use_container_width=True, height=height)


