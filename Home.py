import streamlit as st
from utils.main_options import Options
import cv2
from utils.database import *
from utils.face_detection import *
from streamlit_extras.switch_page_button import switch_page
import time
from utils.sidebar import *


# Run the Streamlit app
if __name__ == "__main__":
    st.title("CheckIn&Out")
    st.markdown("This app uses face recognition to identify users and check them in the workplace.")

    #Create two columns 
    col1,col2 = st.columns([0.7,0.3], gap = 'small')

    # Load options
    options = Options()
    opt = options.parse_args()
    # Initialize options in session state
    st.session_state['options'] = opt

    # Initialize date in session state
    st.session_state['date'] = time.strftime("%Y-%m-%d")

    # Initialize databases paths in session state (will keep them as default)
    if 'users_path' not in st.session_state:
        st.session_state['users_path'] = opt.user_database
    if 'check_in_path' not in st.session_state:
        st.session_state['check_in_path'] = opt.checkin_database

    # Load default databases in session state 
    # Check if the databases are already in session state to avoid reinitializing them every time the script is run
    if 'users_database' not in st.session_state:
        if os.path.exists(st.session_state['users_path']):
            load_database('users_database')
        else:
            new_database('users_database')

    if 'check_in_database' not in st.session_state:   
        if os.path.exists(st.session_state['check_in_path']):
            load_database('check_in_database')
        else:
            new_database('check_in_database')
        
    
    #Initialize sidebar
    with st.sidebar:
        # Initialize some variables in session state
        if 'load_users_pressed' not in st.session_state:
            st.session_state['load_users_pressed'] = False
        if 'load_checkin_pressed' not in st.session_state:
            st.session_state['load_checkin_pressed'] = False
        if 'new_users_pressed' not in st.session_state:
            st.session_state['new_users_pressed'] = False  
        if 'new_checkin_pressed' not in st.session_state:
            st.session_state['new_checkin_pressed'] = False
        if 'new_user_confirm' not in st.session_state:
            st.session_state['new_user_confirm'] = False
        if 'new_checkin_confirm' not in st.session_state:
            st.session_state['new_checkin_confirm'] = False
        if 'save_user_pressed' not in st.session_state:
            st.session_state['save_user_pressed'] = False
        if 'save_checkin_pressed' not in st.session_state:
            st.session_state['save_checkin_pressed'] = False
        if 'saved_user_database' not in st.session_state:
            st.session_state['saved_user_database'] = False
        if 'saved_checkin_database' not in st.session_state:
            st.session_state['saved_checkin_database'] = False
        
        # Display the sidebar
        database_sidebar()

    # Initialize some variables
    process_this_frame = True

    #Initialize check in and check out flags
    if 'show_check_in' not in st.session_state:
        st.session_state['show_check_in'] = False
    if 'show_check_out' not in st.session_state:
        st.session_state['show_check_out'] = False
    
    # Initialize the recognized user flag (set to true if a known user is detected)
    if 'recognized_user' not in st.session_state:
        st.session_state['recognized_user'] = False
    # Initialize the confirm check flag (set to true if the user confirms the check in/out)
    if 'confirm_check' not in st.session_state:
        st.session_state['confirm_check'] = False

    # If the user database has been correctly loaded, display the main page
    if 'users_database' in st.session_state:     

        with col1:
            # Place a button to start the camera
            start_button = st.button("Check in / Check out", key = 'start')
            if start_button:
                # Add a button to stop the camera
                stop_button_pressed = st.button("Stop") # Button to stop the camera
                st.session_state['frame_placeholder2'] = st.empty()          # Placeholder for the frame
                
        with col2:
            # Add a button to register a new user
            new_user = st.button("Register new user")
            if new_user:
                stop_button_pressed = True      #Stop acquisition
                # Switch to the New User page
                switch_page("new user")
        

        with col1:
            if start_button:
                # Start the camera
                video_capture = cv2.VideoCapture(0)
                # Initialize i to count the number of frames the same user is detected
                i = 0
                st.session_state['previous_user'] = None    # Initialize previous user
                
                while video_capture.isOpened() and not stop_button_pressed:
                    ret, st.session_state['main_frame'] = video_capture.read()
                    if not ret:
                        # If the frame is not read, break the loop
                        break
                    
                    if process_this_frame:
                        # Find all the faces and face encodings in the current frame of video
                        st.session_state['face_loc'], st.session_state['face_names'] = process_frame(st.session_state['main_frame'])
                        
                        
                    # Only process every other frame of video to save time
                    process_this_frame = not process_this_frame

                    #Display results on the main frame
                    display_results_st(st.session_state['main_frame'], st.session_state['face_loc'], st.session_state['face_names'], st.session_state['frame_placeholder2'])

                    # If multiple faces are detected, display a warning
                    if len(st.session_state['face_names'])>1:
                            st.warning("Multiple faces detected. Please show only one face at a time.")

                    # If a known user is detected, check if the user is the same for 5 consecutive frames
                    if len(st.session_state['face_names']) == 1 and 'Unknown' not in st.session_state['face_names']:
                        st.session_state['current_user'] = st.session_state['face_names'][0]
                        
                        if st.session_state['current_user'] != st.session_state['previous_user']:
                            i = 0
                            st.session_state['previous_user'] = st.session_state['current_user']
                                
                        else:
                            i += 1

                    # If the same user is detected for 5 consecutive frames, set the recognized_user flag to True and stop the camera
                    if i == 5:
                        st.session_state['recognized_user'] = True
                        stop_button_pressed = True

                    if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
                        break

        with col2:
            # If recognized_user is True, display the check in/out options
            if st.session_state['recognized_user']:
                # Keep displaying the main frame with the user's name
                display_results_st(st.session_state['main_frame'], st.session_state['face_loc'], st.session_state['face_names'], st.session_state['frame_placeholder2'])
                
                # Check if the user is already checked in or out
                mes = check_in_out(st.session_state['current_user'])
                st.write(f'{mes} available for {st.session_state["current_user"]}.')

                # Add buttons to check in or out or cancel
                check_button_pressed = st.button(f"Confirm {mes}", key='check_in')
                exit_button_pressed = st.button("Don't confirm", key='exit')

                if check_button_pressed:
                    # Proceed to check in/out
                    st.session_state['confirm_check']  = True
                
                if exit_button_pressed:
                    # Reset the flags
                    st.session_state['recognized_user'] = False
                    st.session_state['confirm_check'] = False
                    
                if st.session_state['confirm_check']:
                    # Display the check in/out options
                    if st.session_state['show_check_in']:
                        # Check in user
                        suc = add_check_in(st.session_state['current_user'])
                        st.write(suc)
                        # Reset the flags
                        st.session_state['show_check_in'] = False
                        st.session_state['confirm_check'] = False
                        st.session_state['recognized_user'] = False

                    elif st.session_state['show_check_out']:
                        # Check out user
                        suc = add_check_out(st.session_state['current_user'])
                        st.write(suc)
                        # Reset the flags
                        st.session_state['show_check_out'] = False
                        st.session_state['confirm_check'] = False
                        st.session_state['recognized_user'] = False


    
