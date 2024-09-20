import streamlit as st
from utils.main_options import Options
import cv2
from utils.database import *
from utils.face_detection import *
import time
from utils.sidebar import *


if __name__ == '__main__':
    st.markdown("## Register new user")
    # Load options
    options = Options()
    opt = options.parse_args()
    # Initialize options in session state if not already initialized
    if 'options' not in st.session_state:
        st.session_state['options'] = opt

    # Always reset submit button pressed
    st.session_state['submit_button_pressed'] = False

    # Initialize reset in session state, this button allows to register a new user
    if 'reset' not in st.session_state:
        st.session_state['reset'] = False

    # Initialize whether the photo button was pressed
    if 'photo_button_pressed' not in st.session_state:
        st.session_state['photo_button_pressed'] = False

    process_this_frame = True

    # Buttons to start camera and take picture
    start_button = st.button("Start camera")
    photo_button = st.button("Take picture")

    # Start camera
    video_capture = cv2.VideoCapture(0)
    frame_placeholder = st.empty()
    stop_button_pressed = st.button("Stop")

    if start_button:
        # Start the camera
        while video_capture.isOpened() and not stop_button_pressed and not photo_button:
        
            ret, st.session_state['frame'] = video_capture.read()
           
            if not ret:
                break
            
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                st.session_state['face_locations'], st.session_state['face_names'] = process_frame(st.session_state['frame'])
            process_this_frame = not process_this_frame

            # Display the results
            display_results_st(st.session_state['frame'], st.session_state['face_locations'], st.session_state['face_names'], frame_placeholder)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            
        video_capture.release()
        cv2.destroyAllWindows() 

   
    if photo_button:
        # Take a picture and display the results
        st.session_state['photo_button_pressed'] = True
        display_results_st(st.session_state['frame'], st.session_state['face_locations'], st.session_state['face_names'], frame_placeholder)
        
        # Check if the picture has the right format
        if len(st.session_state['face_encodings'])==0:
            st.warning("Error: please take a new picture.")
        
        if len(st.session_state['face_names'])>1:
            st.warning("Multiple faces detected. Please show only one face at a time.")

        if len(st.session_state['face_names'])>0 and st.session_state['face_names'][0] != 'Unknown':
            st.warning(f"User {st.session_state['face_names'][0]} already in database.")

        elif len(st.session_state['face_names'])==0:
            st.warning("No face detected. Please take a new picture.")

        else:
            # If the picture is right, display the form to register the new user
            st.session_state['reset'] = True

    if st.session_state['photo_button_pressed'] and st.session_state['reset'] == True:
        # Display the form to register the new user
        with st.form("user_info"):
            st.write("Register new user")
            # Add a text input to enter the new user name
            name = st.text_input("Enter new user name", key='user_name')
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                st.session_state['submit_button_pressed'] = True
                st.session_state['name'] = name
                # Check if the user name is already in the database
                if st.session_state['name'] in st.session_state['users_database']:
                    st.warning(f"User {st.session_state['name']} already in database. Provide a different username.")

                else:
                    # Add the new user to the database
                    st.write(f"Form submitted successfully! New user name: {st.session_state['name']}")
                    new_user(st.session_state['name'], st.session_state['face_encodings'])
                    print(f"User {st.session_state['name']} added successfully!")
                    # Reset flag to remove the form
                    st.session_state['reset'] = False
            else:
                # Reset submit button pressed
                st.session_state['submit_button_pressed'] = False