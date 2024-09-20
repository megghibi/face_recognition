''' This script defines the options that are used in the main script. 
It is used to parse the arguments that are passed to the main script.+

The options are:
- dataroot: path to the database
- new_dataroot: path to save updated database
- resize_frames: whether frames should be resized for more efficient computations'''

import argparse

class Options():

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Script options")
        self._add_arguments()

    def _add_arguments(self):
        """Define the common options that are used in both training and test."""
        # basic parameters
        self.parser.add_argument('--user_database', default = '.\Data\default_users_database.pkl', help='path to database')
        self.parser.add_argument('--checkin_database', default = '.\Data\default_checkin_database.pkl', help='path to checkin database')
        self.parser.add_argument('--resize_frames', type=bool, default= False, help='Whether frames should be resized for more efficient computations')

    def parse_args(self):
        return self.parser.parse_args()
    