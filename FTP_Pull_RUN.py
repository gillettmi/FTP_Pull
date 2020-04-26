#!/usr/bin/env python3

# This program automates the downloading of files from a remote FTP site
# Written by Michael Gillett, 2019

# LOGIN INFORMATION ====================================================================================================

# Login information and server URL /// Input your own information here if you don't want to have to do it every time
username = ''
password = ''
ftp_url = ''

# Remote locations to pull files from
# if you want to pull from more than one directory, uncomment and change the section(s) below
remote_directories = []

# PROGRAM SETTINGS= ====================================================================================================

# File extensions /// Specify which file extensions you want the program to look for
extensions = ('.mp4', '.mpg', '.mov')

# Set overwrite to True if you would like to overwrite files that may be incomplete downloads.
overwrite = True

# Pull only the most recent file. Set to "False" if you want to pull everything.
pull_recent = True

# RUN ==================================================================================================================

# Program functions are located in ./ftp_functions.py
if __name__ == '__main__':
    if username == '':
        username = input('Username:')
    if password == '':
        password = input('Password:')
    if ftp_url == '':
        ftp_url = input('FTP URL:')
    if remote_directories:
        pass
    else:
        remote_directories = input('Directories to check (Separate with commas):')
        remote_directories = remote_directories.split(',')
    from ftp_functions import *
    main(username, password, ftp_url, remote_directories, extensions, overwrite)
