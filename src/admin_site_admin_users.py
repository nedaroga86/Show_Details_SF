import re
import streamlit as st


from st_aggrid import GridOptionsBuilder, AgGrid
import time

from streamlit_space import space

from cache_manager import manage_cache
from buttons_design import eliminate_button, new_button
from database_class import Data_Base_class



def manage_Users():
    manage_cache()
    db = Data_Base_class()
    users_DB = db.get_all_users_info('id,name,role,area, active')
    st.markdown('''### Users Manager ''')
    col, col2,col3 = st.columns([20,1,12])
    with (col):
        users_DB.reset_index(inplace=True)
        users_DB.rename(columns={'username': 'Username',
                                 'name': 'Full name',
                                 'role': 'Role',
                                 'email': 'Email'}, inplace=True)


        selected_user = show_current_users(users_DB)


        with col3:
            space(lines=1)
            disabled, name, user_id = select_user(selected_user)
            with st.form("Update Password User", clear_on_submit=True):
                new_password = st.text_input("New Password", type="password", disabled=disabled)
                submitted = st.form_submit_button("Reset Password", disabled=disabled)
                if not disabled:
                    if submitted and len(new_password) >0 :
                        db.update_user_password(new_password,user_id)
                        st.success("Your password was updated.")
                    else:
                        st.info(f'Please, provide a new password for the user {name}')
                else:
                    st.warning(f'To reset the password, you should select the user to be updated or deleted')

            c1, c2 = st.columns([5,5])
            with c1:
                if selected_user["selected_rows"] is not None:
                    active = eliminate_button('Active/Deactivate User')
                    value =selected_user["selected_rows"]['active'].iloc[0]
                    if active:
                        value = 0 if value == 1 else  1
                        db.deactivate_user(user_id,int(value))
                        st.session_state['deleted_msg'] = True


            if 'deleted_msg' in st.session_state:
                st.success(f'The user {name} with the id: "{user_id}" was deleted.')
                del st.session_state['deleted_msg']
                time.sleep(2)
                st.rerun()

        cre, cre2 = st.columns([2,8])
        with cre:
            create_user= new_button('Create User')
            if create_user:
                create_new_user(db, users_DB)


def select_user(selected_user):
    if selected_user["selected_rows"] is not None:
        name = selected_user["selected_rows"]['Full name'][0]
        username = selected_user["selected_rows"]['id'][0]
        disabled = False
        st.markdown(f'###### Reset Password for {name}')
    else:
        name = ''
        username = ''
        disabled = True
        st.markdown(f'Please, Select an user to reset password or delete')
    return disabled, name, username


@st.dialog('Create User',width="large")
def create_new_user(db, users_DB):

    with st.form("New User", clear_on_submit=True):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        role = st.selectbox("Role", ("Admin", "User"))
        but1,but2, but3 = st.columns([2,6,2])

        submitted = but3.form_submit_button("Create", use_container_width=True)
        cancel = but1.form_submit_button("Cancel", use_container_width=True)

        if submitted:
            if not _is_valid_email(email):
                st.warning("Please enter a valid email address.")
            elif email in users_DB['Email'].to_list():
                st.error('User already exists')
            elif email is '' or name is '' or password is '' or role is '':
                st.error('Please, all requested fields to create the user')
            else:
                username = email.split("@")[0]
                db.create_new_user(email, name, password, role, username)
                st.success(f'User {name}: {email} created successfully')
                time.sleep(1)
                st.rerun()
        if cancel:
            st.rerun()


def _is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def show_current_users(users_DB):
    db = Data_Base_class()
    st.markdown(
        """
        <style>
        .custom-container {
            background-color: #f0f0f0; /* Color gris claro */
            padding: 20px;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True)
    with st.container(border=False):
        quick_filter_text = st.text_input("Filtrar filas:", "")
        #st.markdown("Users with access to the 5Y Forecasting Tool")
        gb = GridOptionsBuilder.from_dataframe(users_DB)
        gb.configure_column('index', width=80, sort='asc')
        gb.configure_column('id', width=100)
        gb.configure_column('Full name', header_name='Full Name', filter=True,width=200)
        gb.configure_column('Role', width=100)
        gb.configure_column('area', width=100)
        gb.configure_column('active', width=80)
        gb.configure_selection(use_checkbox=True,
                               header_checkbox=True,
                               header_checkbox_filtered_only=True)

        gb.configure_grid_options(domLayout='fill')  # Ajuste de tamaño normal
        gb.configure_grid_options(rowHeight=25)  # Ajustar altura dinámica
        gb.configure_grid_options(quick_filter=quick_filter_text)  # Ajustar altura dinámica
        gridOptions = gb.build()
        selected_user =AgGrid(users_DB, gridOptions=gridOptions,
                              height=500,
                              allow_unsafe_jscode=True,
                              fit_columns_on_grid_load=True)

        return  selected_user






