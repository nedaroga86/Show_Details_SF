import os
import streamlit as st


from streamlit_option_menu import option_menu
from conf_page import set_config_page
from tables_opportunities import show_opportunities_table
from tables_opportunity_source import show_opportunity_source_table
from tables_leads import show_leads_table
from tables_converted_leads import show_converted_leads

st.cache_data.clear()
st.cache_resource.clear()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
icon =  os.path.join(BASE_DIR, '..', 'images','logo.ico')




class Main_Program:
    def get_start(self):
        set_config_page()
        menu_styles = {
            "container": {"padding": "2px", "background-color": "#fafafa"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "center",
                "margin": "5px",
                "hover-color": "#fafafa",
                "icon": {"color": "red"}
            },
            "nav-link-selected": {"background-color": "#ED2E17", "color": "white"}, #9E3E4A
            "icon": {"color": "#F0F0F0"},
            "nav-link-logout": {"color": "red", "hover-color": "#ffcccc"},
        }
        page = option_menu(None, ["New Pipeline Tables" , "Opportunity Source", "Lead Tables","Converted Leads","Logout"],
                           icons=['bi bi-list-task','bi bi-list-task','bi bi-list-task'],
                           menu_icon="menu-up", default_index=0, orientation="horizontal",
                           styles=menu_styles)


        if page == "New Pipeline Tables":
            st.title('New Pipeline')
            st.markdown('This page is for the Start Pipeline Tables')
            show_opportunities_table()

        elif page == "Opportunity Source":
            st.title('Opportunity Source')
            st.markdown('This page is for the Opportunity Source Tables: New customer, Existing customer, and Lost with marketing source filter')
            show_opportunity_source_table()

        elif page == "Lead Tables":
            st.title('Lead Tables')
            st.markdown('This page is for the Lead Tables')
            show_leads_table()


        elif page == "Converted Leads":
            st.title('Converted Leads')
            st.markdown('This page is for the Converted Leads Tables')
            show_converted_leads()



