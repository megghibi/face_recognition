import streamlit as st
from utils.database import *
import os
import time
from utils.main_options import Options
import pickle


def database_sidebar():

    # Add a button to load a new users database from file explorer
    load_users = st.button("Load existing user database", type="primary", use_container_width=True, key='load_users_button')
    if load_users:
        # Set the load_users_pressed session state to True
        st.session_state['load_users_pressed'] = True
    
    if st.session_state['load_users_pressed']:
        # Display a file uploader to load a .pkl file
        uploaded_file = st.file_uploader("Choose a .pkl file", type="pkl", key="users_upload")

        # If a file is uploaded, load the users database
        if uploaded_file is not None:
            st.session_state['users_database'] = pickle.load(uploaded_file)
            st.write('Successfully loaded users database')
            # Reset the users path and saved_user_database session states
            st.session_state['users_path'] = None       # Reset to None to avoid overwriting the loaded database
            st.session_state['saved_user_database'] = False
            st.session_state['load_users_pressed'] = False

    # Add a button to load a new checkin database from file explorer
    load_checkin = st.button("Load existing check-in database", type="primary", use_container_width=True, key='load_checkin_button')
    if load_checkin:
        st.session_state['load_checkin_pressed'] = True

    if st.session_state['load_checkin_pressed']:
        # Display a file uploader to load a .pkl file
        uploaded_file = st.file_uploader("Choose a .pkl file", type="pkl", key="checkin_upload")
        if uploaded_file is not None:
            st.session_state['check_in_database'] = pickle.load(uploaded_file)
            st.write('Successfully loaded check-in database')   
            st.session_state['check_in_path'] = None
            st.session_state['saved_checkin_database'] = False
            st.session_state['load_checkin_pressed'] = False

    # Add a button to create a new users database
    new_users_database = st.button("New user database", type="primary", use_container_width=True, key='new_users_button')
    if new_users_database:
        # Set the new_users_pressed session state to True and the new_user_confirm session state to False
        st.session_state['new_users_pressed'] = True
        st.session_state['new_user_confirm'] = False

    if st.session_state['new_users_pressed'] and not st.session_state['new_user_confirm']:
        # Add a button to confirm the creation of a new users database
        confirm_users = st.button("Confirm? Current data will be replaced.", use_container_width=True, key="confirm_users")
        if confirm_users:
            # Create a new users database using the new_database function
            new_database('users_database')
            st.write('Successfully created new users database')
            st.session_state['saved_user_database'] = False
            st.session_state['new_users_pressed'] = False
            st.session_state['new_user_confirm'] = True

    # Add a button to create a new check-in database
    new_checkin_database = st.button("New check-in database", type="primary", use_container_width=True, key='new_checkin_button')
    if new_checkin_database:
        st.session_state['new_checkin_pressed'] = True
        st.session_state['new_checkin_confirm'] = False

    if st.session_state['new_checkin_pressed']:
        confirm_checkin = st.button("Confirm? Current data will be replaced.", use_container_width=True, key="confirm_checkin")
        if confirm_checkin:
            new_database('check_in_database')
            st.session_state['saved_checkin_database'] = False
            st.session_state['new_checkin_pressed'] = False
            st.session_state['new_checkin_confirm'] = True
            st.write('Successfully created new check-in database')

    # Add download button to save selected database only if it is not saved yet
    if 'users_database' in st.session_state and st.session_state['users_database'] is not None and st.session_state['saved_user_database'] is False:
        save_button = st.button("Save user database", type="primary", use_container_width=True, key='save_button1')
        if save_button:
            # Set the save_user_pressed session state to True
            st.session_state['save_user_pressed'] = True
    
        if st.session_state['save_user_pressed']:
            filename = ''

            # Add checkboxes to allow the user to save the database with a 'default' or with the current date at the beginning of the filename
            default = st.checkbox("Save as default database", key ='def1')
            if default:
                filename += 'default'

            date = st.checkbox("Save with date", key='date1')
            if date:
                filename += st.session_state["date"]
            
            # Display a download button to save the users database as a .pkl file
            save_users = st.download_button(
                "Save user data",
                data=pickle.dumps(st.session_state['users_database']),
                file_name=f'{filename}_users_database.pkl',
                use_container_width=True,
                key='save_users_button'
            )
            if save_users:
                # When the database is saved, set the saved_user_database session state to True and the save_user_pressed session state to False
                st.session_state['saved_user_database'] = True
                st.session_state['save_user_pressed'] = False


    
    if 'check_in_database' in st.session_state and st.session_state['check_in_database'] is not None and st.session_state['saved_checkin_database'] is False:
        save_button = st.button("Save check-in database", type="primary", use_container_width=True, key='save_button2')
        if save_button:
            st.session_state['save_checkin_pressed'] = True

        if st.session_state['save_checkin_pressed']:
            filename = ''
            default = st.checkbox("Save as default database", key='def2')
            if default:
                filename += 'default'
                
            date = st.checkbox("Save with date", key='date2')
            if date:
                filename += st.session_state["date"]

            print(st.session_state['check_in_database'])
            save_checkin = st.download_button(
                "Save check-in data",
                data=pickle.dumps(st.session_state['check_in_database']),
                file_name=f'{filename}_check_in_database.pkl',
                use_container_width=True,
                key='save_checkin_button'
            )
            if save_checkin:
                st.session_state['saved_checkin_database'] = True
                st.session_state['save_checkin_pressed'] = False


