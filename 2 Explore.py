import streamlit as st

# Place a checkbox to select which database to display
st.markdown("## Explore")
st.markdown("### Select database to display")  
database = st.selectbox("Database", ['Users', 'Check-ins'])

# Initialize if the remove user button was pressed
if 'remove_user_button_pressed' not in st.session_state:
    st.session_state['remove_user_button_pressed'] = False

# If selected database is users, display users names as a numbered list
if database == 'Users':
    # Place a button to remove a user
    pop = st.button("Remove user", key='pop')
    if pop:
        # If the button is pressed, set the flag to True
        st.session_state['remove_user_button_pressed'] = True
        
    if st.session_state['remove_user_button_pressed']:
        # Place a dropdown to select the user to remove (will be removed as soon as the user is selected)
        user_to_remove = st.selectbox("Select users to remove", ['None'] + list(st.session_state['users_database'].keys()))

        # If a user is selected, store the user name in session state
        if user_to_remove != 'None':
            st.session_state['user_to_remove'] = user_to_remove
            print(st.session_state['user_to_remove'])
        
        # If the user is selected, remove the user from the user database and from the check-in database
        if 'user_to_remove' in st.session_state:
            print(st.session_state['user_to_remove'])
            st.session_state['users_database'].pop(st.session_state['user_to_remove'])
            for date in st.session_state['check_in_database']:
                if st.session_state['user_to_remove'] in st.session_state['check_in_database'][date]:
                    st.session_state['check_in_database'][date].pop(st.session_state['user_to_remove'])
            st.session_state['remove_user_button_pressed'] = False
            
            # Delete the 'user_to_remove' key from session state
            st.session_state.pop('user_to_remove')

    st.markdown("#### Available users in database")
    if 'users_database' in st.session_state:
        # Display the users in the database
        for n in range(len(st.session_state['users_database'])):
            st.write(f'{n+1}. {list(st.session_state["users_database"].keys())[n]}')
    else:
        st.write("No users in database")

# If selected database is check-ins, display check-ins as a table
if database == 'Check-ins':
    st.markdown("#### Check-ins in database")
    # Display the check-ins in the database
    if 'check_in_database' in st.session_state:
        st.write(st.session_state['check_in_database'])
    else:
        st.write("No check-ins in database")
