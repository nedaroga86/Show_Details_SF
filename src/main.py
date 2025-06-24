import os
import streamlit as st

from conf_page import set_config_page


st.cache_data.clear()
st.cache_resource.clear()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
icon =  os.path.join(BASE_DIR, '..', 'images','logo.ico')




class Main_Program:
    def get_start(self):
        set_config_page()
        with st.sidebar:
            st.text('Navigation:')
        pages = {
            "Opportunities": [
                st.Page("tables_opportunities.py", title="Opportunities Tables"),
                st.Page("tables_opportunity_source.py", title="Opportunity Source Tables")
            ],
            "Leads": [
                st.Page("tables_leads.py", title="Leads Tables"),
                st.Page("tables_converted_leads.py", title="Converted Tables")
            ],
        }
        pg = st.navigation(pages)
        pg.run()




