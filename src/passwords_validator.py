import re
import streamlit as st
import bcrypt

from database_class import Data_Base_class


def validate_passwords(current_password, new_password, confirm_password):
    errors = []
    db = Data_Base_class()
    users_DB = db.get_all_users_info('*')
    user = users_DB[users_DB["id"] == st.session_state.id]
    password_hash = user["password"].iloc[0]
    if isinstance(password_hash, str):
        password_hash = user["password"].iloc[0].encode('utf-8')
    if not bcrypt.checkpw(current_password.encode('utf-8'), password_hash):
        errors.append("The Current Password is incorrect.")

    # Validate length
    if len(new_password) < 8:
        errors.append("The password must be at least 8 characters long.")

    # Validate uppercase letter
    if not re.search(r'[A-Z]', new_password):
        errors.append("The password must contain at least 1 uppercase letter (A-Z).")

    # Validate lowercase letter
    if not re.search(r'[a-z]', new_password):
        errors.append("The password must contain at least 1 lowercase letter (a-z).")

    # Validate number
    if not re.search(r'[0-9]', new_password):
        errors.append("The password must contain at least 1 number (0-9).")

    # Disallow invalid special symbols
    if re.search(r'[^a-zA-Z0-9@#$%&*]', new_password):
        errors.append("The allowed special symbols are (@, #, $, %, &, *).")
    # Validate special symbol
    elif not re.search(r'[\@\#\$\%\&\*]', new_password):
        errors.append("The password must contain at least 1 special symbol (@, #, $, %, &, *).")


    if re.search(r'(.)\1{2,}', new_password):
        errors.append("The password must not contain repeated characters (e.g., 'aaa').")

    if any(seq in new_password.lower() for seq in ["1234", "abcd", "qwerty", "password", "admin"]):
        errors.append("The password must not contain common sequences or weak words (e.g., 'abcd', '1234', 'password').")

    if (re.search(r'(012|123|234|345|456|567|678|789|890|901|987|876|765|654|543|432|321|210)', new_password) or
            re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz'
                 r'|zyx|yxw|xwv|wvu|vut|uts|tsr|srq|rqp|qpo|pon|onm|nml|mlk|lkj|kji|jih|ihg|hgf|gfe|fed|edc|dcb|cba)', new_password.lower())):
        errors.append("The password must not contain sequences (e.g., 'abcd', '1234')")

    # Check if new password matches the current password
    if new_password == current_password:
        errors.append("The new password cannot be the same as the current password.")

    # Check if passwords match
    if new_password != confirm_password:
        errors.append("The passwords do not match.")

    return errors