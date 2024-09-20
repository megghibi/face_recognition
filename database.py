# This module is useful for database functions

# load_database: opens dictionary stored as pickle file in the specified dataroot
# new_database: creates a dictionary to store new users
# save_database: saves dictionary as pickle file in the specified dataroot
# User: creates a new user with the specified encoding and home flag
# new_user: adds a new user to the database
# checkin: checks in a user
# checkout: checks out a user

import pickle
import time
import streamlit as st

'''
Database functions'''

@st.cache_resource
def load_database(type=['users_database', 'check_in_database']):
    '''This function loads the database from the specified path.'''
    # Check if the database type is valid
    if type not in ['users_database', 'check_in_database']:
        raise ValueError("Invalid database type. Must be either 'users_database' or 'check_in_database'.")
    
    # Load the database from the specified path as pickle file
    if type == 'users_database':
        with open(st.session_state['users_path'], 'rb') as f:
            st.session_state[type] = pickle.load(f)

    elif type == 'check_in_database':
        with open(st.session_state['check_in_path'], 'rb') as f:
            st.session_state[type] = pickle.load(f)
    
    # If the database is None type, create a new database
    if st.session_state[type] is None:
        new_database(type)
        st.warning(f'No {type} found. Created a new {type}.')
        
    f.close()


@st.cache_data
#Unused
def save_database(type=['users_database', 'check_in_database']):
    '''This function saves the database to the data path.'''
    # Check if the database type is valid
    if type not in ['users_database', 'check_in_database']:
        raise ValueError("Invalid database type. Must be either 'users_database' or 'check_in_database'.")
    
    # 
    elif type == 'users_database':
        with open(st.session_state['users_path'], 'wb') as f:
            pickle.dump(st.session_state[type], f)

    elif type == 'check_in_database':
        with open(st.session_state['check_in_path'], 'wb') as f:
            pickle.dump(st.session_state[type], f)

    f.close()

@st.cache_data
def new_database(type=['users_database', 'check_in_database']):
    '''This function creates a new database locally but does not save it externally.'''
    st.session_state[type] = {}

'''
User functions'''
@st.cache_data
def User(encoding):
    '''This function creates a new user with the specified encoding and home flag.
    This function is called by the new_user function.'''
    
    user = {'encoding': encoding}   #Encoding for user
           
    return user

@st.cache_data
def new_user(name, encoding):
    """
    Add a new user to the database.

    Args:
        name (str): The name of the user.
        encoding (str): The encoding to use for the user.

    Returns:
        None
    """
    # Create a new user
    user = User(encoding)
    #print(name, user)
    #print(type(st.session_state['users_database']))

    # Add the user to the database using the name as the key
    st.session_state['users_database'][name] = user


'''
Check in functions'''

def check_in_out(user):
    '''This function evaluates whether the user is checking in or out.'''
    # Get the current date
    date = st.session_state['date']

    # If it is the first check in of the day, set check_in flag to True
    if date not in st.session_state['check_in_database']:
        st.session_state['show_check_in'] = True
        return 'Check in'
    
    elif date in st.session_state['check_in_database']:
    # If it is not the first check in of the day, check if the user has checked in already
        if user in st.session_state['check_in_database'][date]:
            # Check if user has an open check in event during the day
            if st.session_state['check_in_database'][date][user][-1]['Check-out'] == None:
                st.session_state['show_check_out'] = True
                return 'Check out'
            else:
                # If user has checked out, set check_in flag to True
                st.session_state['show_check_in'] = True
                return 'Check in'

        else:
            # If user has not checked in yet today, set check_in flag to True
            st.session_state['show_check_in'] = True
            return 'Check in'
            
    else:
        # In case everything fails, return 'Nothing'
        return 'Nothing'

#@st.cache_data
def add_check_in(user):
    '''
    This function adds a check in or check out event to the check in database.
    
    Args:
        user (str): The name of the user.
        check_in (bool): A flag indicating whether the user is checking in.
        check_out (bool): A flag indicating whether the user is checking out.
        
    Returns:
        None'''
    
    # Get the current date
    date = st.session_state['date']

    #Create a new check in event
    checkin = {'Check-in': time.strftime("%H:%M:%S"),
                'Check-out': None,
                }

    # Add check in information to database if it is the first check in of the day
    if date not in st.session_state['check_in_database']:
        # Create a new date key in the database
        st.session_state['check_in_database'][date] = {}
        # Create a new user key in the date key and assign the check in event
        st.session_state['check_in_database'][date][user] = [checkin]

        # Reset check in flag
        st.session_state['show_check_in'] = False
        return f'{user} successfully checked in {time.strftime("%H:%M:%S")}.'     
    else:
        # Add check in information to database if it is user's first check in of the day
        if user not in st.session_state['check_in_database'][date]:
            # If user is not checked in today, create a new user key in the date key and assign the check in event
            st.session_state['check_in_database'][date][user] = [checkin]

            # Reset check in flag
            st.session_state['show_check_in'] = False
            return f'{user} successfully checked in at {time.strftime("%H:%M:%S")}.'     
        
        # Add additional check in information for multiple check ins
        else:
            # If user has already checked in today, append the check in event to the user key
            st.session_state['check_in_database'][date][user].append(checkin)
            # Reset check in flag
            st.session_state['show_check_in'] = False
            return f'{user} successfully checked in {time.strftime("%H:%M:%S")}.'     


#@st.cache_data
def add_check_out(user):     

    # Get the current date
    date = st.session_state['date']

    # Add check out time to last check in event
    st.session_state['check_in_database'][date][user][-1]['Check-out'] = time.strftime("%H:%M:%S")
    # Reset check out flag
    st.session_state['show_check_out'] = False
    return (f'{user} successfully checked out at {time.strftime("%H:%M:%S")}.')
        
    

