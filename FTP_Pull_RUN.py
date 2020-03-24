#!/usr/bin/env python3

# This program automates the downloading of files from a remote FTP site
# Written by Michael Gillett, 2019

# LOGIN INFORMATION ====================================================================================================

# Login information and server URL /// Input your own information here
username = ''
password = ''
ftp_url = 'ftp.website.com'

# Remote locations to pull files from
# if you want to pull from more than one directory, uncomment and change the section(s) below
remote_directories = (
    '~/directory/directory1',
    # '~/directory1/directory2',
    # '~/directory1/directory3',
)

# PROGRAM SETTINGS= ====================================================================================================

# File extensions /// Specify which file extensions you want the program to look for
extensions = ('.mp4', '.mpg', '.mov')

# Set overwrite to True if you would like to overwrite files that may be incomplete downloads.
overwrite = True

# RUN ==================================================================================================================

# Program functions are located in ./ftp_functions.py
if __name__ == '__main__':
    from ftp_functions import *
    main(username, password, ftp_url, remote_directories, extensions, overwrite)
