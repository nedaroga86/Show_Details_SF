import os
import sqlite3

import bcrypt
import pandas as pd
import streamlit as st
from streamlit_space import space

from main_app import call_main_app

st.cache_data.clear()
st.cache_resource.clear()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
icon =  os.path.join(BASE_DIR, '..', 'images','icon.ico')


page_bg_img = """
<style>
/* Change the background image */
[data-testid="stAppViewContainer"] {
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Optionally, set a background color */
[data-testid="stAppViewContainer"] {
    background-color: #D9D9D9; /* Change to your preferred color */
}

/* Optional: change sidebar background */
[data-testid="stSidebar"] {
    background-color: #f8f9fa; /* Change to your preferred sidebar color */#f8f9fa
}
</style>
"""




class Logging:

    def __init__(self):
        self.users_DB = None
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.BASE_DIR, '..', 'dataBase', 'users.db')

    def show_description(self):


        st.markdown(
            "<h2 style='color: ##EB1700; font-size: 50px;'>Table Details (Monthly Metrics) </h2>",
            unsafe_allow_html=True
        )

        # Add the description with Markdown
        st.markdown("""
            <style>
            .descripcion {
                font-size: 18px;
                line-height: 1.6;
                text-align: justify;
                color: #4D4D4D; /* Cambia el color según lo necesites */
                padding-right: 80px;
                border-radius: 10px;
            }
            </style>
            <div class="descripcion">
            Our platform is designed to provide detailed visibility into the data presented in the monthly reports. 
            It allows you to explore sales performance with clarity, offering a deeper understanding of key metrics 
            across dimensions such as Customer Cohorts, Sales Trends, and Revenue Metrics.
            <br><br>
            By leveraging historical data and advanced analytics, you can uncover trends, track behavioral patterns, 
            and measure performance across specific periods. This detailed view supports more accurate interpretation 
            of the monthly summaries and enables better data-driven decision-making to refine your commercial strategies.
                <br><br>
            </div>
            """, unsafe_allow_html=True)


    def main(self):

        if self.users_DB is None:
            conn = sqlite3.connect(self.db_path)
            self.users_DB = pd.read_sql_query("SELECT * FROM users_table", conn)
            conn.close()


        auth_container = st.empty()
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
            st.session_state.recur_status = False


        if not st.session_state.logged_in:
            st.set_page_config(page_title="Details Table Analysis", layout= 'wide', page_icon=icon, initial_sidebar_state="collapsed")
            with auth_container.container():
                logo =  os.path.join(BASE_DIR, '..', 'images','logo.png')
                st.logo(logo)
                st.text("")
                test, test2 = st.columns(2)
                with test:
                    space( lines=10)
                    self.show_description()
                with test2:
                    space( lines=15)
                    st.markdown(page_bg_img, unsafe_allow_html=True)
                    st.markdown(
                        """
                        <style>
                        label {
                            color: #4D4D4D !important; 
                            font-size: 16px !important; 
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    app_version = "v3.5.0"
                    st.markdown(
                        f"""
                                <style>
                                    .footer {{
                                        position: fixed;
                                        bottom: 0;
                                        left: 0;
                                        width: 100%;
                                        text-align: left;
                                        color: gray;
                                        padding: 10px;
                                        font-size: 18px;
                                        background-color: #f9f9f9;
                                    }}
                                </style>
                                <div class="footer">Version: {app_version}</div>
                                """,
                        unsafe_allow_html=True
                    )
            if len(username) > 0 and len(password) > 0:
                if username in self.users_DB['id'].to_list():
                    user = self.users_DB[self.users_DB["id"] == username]
                    password_hash = user["password"].iloc[0]
                    if isinstance(password_hash, str):
                        password_hash = user["password"].iloc[0].encode('utf-8')
                    if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                        st.session_state.clear()
                        st.session_state.id = username
                        st.session_state.role = user["role"].iloc[0]
                        st.session_state.users_DB = self.users_DB
                        st.session_state.name = user["name"].iloc[0]
                        st.session_state.area = user["area"].iloc[0]
                        st.session_state.logged_in = True
                        st.session_state.recur_status = False
                        auth_container.empty()
                    else:
                        with test2:
                            st.error("Authentication failed")
                else:
                    with test2:
                        st.info("Press enter to login")

        if st.session_state.logged_in:
            st.set_page_config(page_title="Details Table Analysis", layout= 'wide', page_icon=icon, initial_sidebar_state="expanded")
            call_main_app()




if __name__ == "__main__":
    access = Logging()
    access.main()


