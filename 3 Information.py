import streamlit as st

# Place a checkbox to select which database to display
st.markdown("### Instructions")

with st.expander("Homepage", expanded=False):
    st.write("The homepage is the main page of the app. Here, the user can check-in and out. The homepage consists of the following sections:")
    st.write("1. The sidebar allows to navigate to the other pages of the app. Additionally, it allows to handle the user database and check-in database. By default, the app loads the user database and check-in database from the paths specified in the options. If the path is empty, a new database is automatically created. The user can also load a preexisting database, instantiate a new database, and save the current database externally with the download button. To explore the databases, the user can navigate to the 'Explore' page.")
    st.write("2. The 'Check in/Check out' button allows the user to start the check-in procedure. It starts the camera, which automatically detects the user's face. If the user is recognized, the app processes the check-in status of the user from the check-in database and enables a check-in or check-out option, which can be confirmed or not. If the user is not recognized, the new user can be registered by clicking the 'Register new user' button.")
    st.write("3. The 'Register new user' button switches to the 'New user' page, where the user can register a new user.")
    st.write("4. The stop button can be used to stop the camera acquisition.")

with st.expander("New user", expanded=False):
    st.write("The 'New user' page allows the user to register a new user. The page consists of the following sections:")
    st.write("1. The 'Start camera' button starts the camera acquisition. The camera detects the user's face without automatically stopping.")
    st.write("2. The 'Take picture' button allows the user to take a picture of the user's face in an optimal position. This option will return an error if more than one face is detected. A known face will not enable the registration of a new user.")
    st.write("3. The registration procedure is enabled when an unknown face is detected in the picture. The user can enter the name of the new user and click the 'Submit' button to register the new user. If the username is already in the database, the user will be prompted to enter a different name.")
    st.write("The new user is added to the user database and can be checked in on the homepage. The user can also navigate to the 'Explore' page to view the user information.")

with st.expander("Explore", expanded=False):
    st.write("The 'Explore' page allows the user to explore the user database and check-in database. The user can select the database to display from the dropdown menu.:")
    st.write("1. The 'Users' database displays the available users in the database. The user can remove a user by clicking the 'Remove user' button and selecting the user from the dropdown menu. This action will remove the user from the user database and the check-in database.")
    st.write("2. The 'Check-ins' database displays the check-ins in the database.")

st.markdown("### Additional information")
st.write("The app uses the face_recognition library provided by Adam Geitgey at https://github.com/ageitgey/face_recognition . The library is based on dlib's face recognition library.")