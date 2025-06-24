import os
import sqlite3
import streamlit as st
import bcrypt
import pandas as pd


class Data_Base_class:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:  # Si no existe una instancia, se crea
            cls._instance = super(Data_Base_class, cls).__new__(cls)
        return cls._instance


    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.BASE_DIR, '..', 'dataBase', 'users.db')


    def get_all_users_info(self, columns):
        conn = sqlite3.connect(self.db_path)
        users_DB = pd.read_sql_query(f"SELECT {columns} FROM users_table", conn)
        conn.close()
        return users_DB

    def update_user_password(self, new_password,username):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        hashed_pass = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        c.execute("UPDATE users_table SET password = ? WHERE id = ?", (sqlite3.Binary(hashed_pass), username))
        conn.commit()
        conn.close()

    def create_new_user(self, email, name, password, role, username):
        conn = sqlite3.connect(self.db_path)
        try:
            c = conn.cursor()
            hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            c.execute("INSERT INTO users_table (id,name,password,email,role,MFA) VALUES( ?, ?, ?, ?, ?, ?)",
                      (username, name, hashed_pass, email, role, 0))
            conn.commit()
            conn.close()
        except:
            st.error('The username already exist')
            pass
        conn.close()

    def deactivate_user(self, user_id, value):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE users_table SET active = ? WHERE id = ?", (value,user_id,))
        conn.commit()
        conn.close()