import os
import time

import streamlit as st

from conf_page import set_config_page
from passwords_validator import validate_passwords
from database_class import Data_Base_class
from cache_manager import manage_cache
from admin_site_admin_users import manage_Users



class Setup:

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.BASE_DIR, '..', 'DB', 'users.db')
        self.action = ''
        set_config_page()


    def manage_current_User(self, refresh=False):
        col1, col2,col3 = st.columns([1,4,1])
        with col2:
            st.subheader("Change My Password")
            with st.form("Update Password", clear_on_submit=True):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                submitted = st.form_submit_button("Update Password")
                if submitted:
                    errors = validate_passwords(current_password,new_password,confirm_password)
                    if len(errors)==0:
                        db = Data_Base_class()
                        db.update_user_password(new_password,st.session_state.username)
                        st.success("Your password was updated.")
                        time.sleep(2)
                        st.rerun()
                    else:
                        for idx, error in enumerate(errors):
                            st.warning(f'{idx+1}. {error}')

    def setup(self):

        st.sidebar.subheader('Admin console')
        if st.session_state.role == 'Admin':
            section = st.sidebar.radio("Sections:", options=["Security", "Users Management"])
            if section ==  'Security':
                manage_cache()
                self.manage_current_User()
            elif section == 'Users Management':
                manage_Users()
        else:
            section = st.sidebar.radio("Sections:", options=["Security"])
            manage_cache()
            self.manage_current_User()


