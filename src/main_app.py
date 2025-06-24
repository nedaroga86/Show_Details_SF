import os
import streamlit as st


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
icon =  os.path.join(BASE_DIR, '..', 'images','logo.ico')



st.set_page_config(page_title="Details Table Analysis", layout='wide', page_icon=icon, initial_sidebar_state="expanded")


pages = {
    "Opportunities": [
        st.Page("tables_opportunities.py", title="Opportunities"),
        st.Page("tables_opportunity_source.py", title="Opportunities Source"),
    ],
    "Leads": [
        st.Page("tables_leads.py", title="Priority Leads"),
        st.Page("tables_converted_leads.py", title="Converted Leads"),
    ],
}


pg = st.navigation(pages, position="top")
pg.run()



