import cv2
import numpy as np
import face_recognition
from sklearn.metrics.pairwise import cosine_similarity
from utils.database import *
import streamlit as st

def match_faces(database, new_encoding):
    '''
    This function takes as input a database and a new encoding.
    It computes potential matches with known encodings and returns the matched name or 'unknown'.
    
    Args:
        - database: A dictionary containing the encodings and names of known faces.
        - new_encoding: The encoding of the new face to be matched.
        
    Returns:
        - matched_name: The name of the matched face or 'unknown' if no match is found.
    '''

    # Make arrays with encodings and names stored in database
    known_encodings= []
    known_names = []

    # Initialize name as unknown (will remain unknown if no match is found)
    matched_name = "Unknown"
    
    # If no database is provided, return unknown
    if database is None:
        return matched_name
    
    else:
        # Extract encodings and names from database
        for name in database.keys():
            for enc in database[name]['encoding']:
                known_encodings += [enc]
                known_names += [name]

        # If there are known encodings in the database compare with new encoding
        if len(known_encodings) != 0:
            # See if the face is a match for the known faces (returns a list of True/False values for each known face)
            # Face recognition compares faces by calculating the Euclidean distance between the encodings
            matches = face_recognition.compare_faces(known_encodings, new_encoding, tolerance=0.6)

            # Compute cosine similarity between known encodings and new encoding
            face_similarity = [cosine_similarity([kn_enc], [new_encoding]) for kn_enc in known_encodings]

            # Find the index of the best match with highest cosine similarity
            best_match_index = np.argmax(face_similarity)

            #Check if closest encoding is a potential match also based on Euclidean distance
            if matches[best_match_index]:
                matched_name = known_names[best_match_index]

        return matched_name


def detect_faces(frame):
    '''
    This function encodes faces in a given frame.

    Args:
    - frame: The frame containing the faces to be encoded.

    Returns:
    - locations: The locations of the detected faces in the frame.
    - encodings: The encodings of the detected faces in the frame.
    '''
    # Find all the faces and face encodings in the current frame of video
    locations = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame, locations)

    # Save encodings to txt file for pca analysis
    #if len(encodings) >0:
    #    with open('embedding.txt', 'a') as f:
    #        for encoding in encodings[0]:
    #            f.write(str(encoding))
    #            f.write(',')
    #        f.write('\n')
    return locations, encodings


def process_frame(frame):
    '''
    This function is the main processing function and it encapsulates other functions.
    It takes as input a frame and processes it based on session state options.
    
    Args:
        - frame: The frame to be processed.
        
    Returns:
        - face_locations: The locations of the detected faces in the frame.
        - face_names: The names of the detected faces.
    '''
    if st.session_state['options'].resize_frames:
        # Make frame smaller
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #Extract location and encodings of detected faces in the frame
    face_locations, st.session_state['face_encodings'] = detect_faces(rgb_frame)

    #Create an array to store names of detected users
    face_names = []

    # Compare each encoding with known encodings in database
    for enc in st.session_state['face_encodings']:
        # Return matched name or unknown (name to be displayed)
        name = match_faces(st.session_state['users_database'], enc)
        
        #If user is unknown pass
        if name == 'Unknown':
            pass

        # The name is appended to 
        face_names.append(name)
        
    return face_locations, face_names


def display_results_st(frame, face_loc, face_names, frame_placeholder):
    '''
    Display the results of face detection on the given frame.

    Args:
        frame (numpy.ndarray): The frame on which the face detection was performed.
        face_loc (list): A list of tuples representing the locations of the detected faces.
        face_names (list): A list of names corresponding to the detected faces.

    Returns:
        None
    '''

    for (top, right, bottom, left), name in zip(face_loc, face_names):
        if st.session_state['options'].resize_frames:
            # Scale back up face locations since the frame we detected was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        if name != '':
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    frame_placeholder.image(frame, channels="BGR")
    



            