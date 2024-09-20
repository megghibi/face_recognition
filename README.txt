##### READ ME #####

CHECKIN&OUT

CheckIn&Out is a web application developed with Streamlit that enables registered users to clock in and out of their workplace using facial recognition.
It also includes other functionalities such as user registration, and database exploration.
The app works with two databases: one keeps records of users and their facial embeddings for face recognition, the other keeps track of clock in and clock out times.


To run the project, it is necessary to install the required packages listed in the requirements.txt file in this folder.

For the project to correctly function, it is necessary to keep the Home.py page in the same folder as the Pages folder, like it has been provided.
The utils folder contains modules that are called by the app pages for database manipulation, facial recognition and sidebar functionalities. It also contains a main_options module where the user
can specify a default users and check-in database paths; this is useful if one wants to always use the same databases when running the app. In case the paths are not found, the app instantiates new empty databases.
The main_options also allow to specify whether frames should be resized for faster processing. 


To run the application you should be in the same folder as Home.py and run: streamlit run ./Home.py

This will open the application on a webpage using a local host.

Copyright: face_recognition library sourced from Adam Geitgey @ https://github.com/ageitgey/face_recognition

Created by Margherita Barbuti - m.barbuti1@campus.unimib.it

