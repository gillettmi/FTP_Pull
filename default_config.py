#!/usr/bin/env python3

# CONFIG ####################################################################

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

# File extensions /// Specify which file extensions you want the program to look for
extensions = ('.mp4', '.mpg', '.mov')

# Set overwrite to True if you would like to overwrite files that may be incomplete downloads.
overwrite = True

