#!/usr/bin/env python3

# This program automates the downloading of DW programs from a remote FTP site
# Written by Michael Gillett, 2019

#### CONFIG ####################################################################

# Login information and server URL /// Input your own information here
username = ''
password = ''
ftp_url = ''

# Where you want the files to save
local_path = './'

# Remote locations to pull files from
file_pull = '/'
#file_pull-2 = '~/file_pull-2'
#file_pull-3 = '~/file_pull-3'

# File extensions /// Specify which file extensions you want the program to look for
extensions = ('.txt')

# Set overwrite to True if you would like to overwrite files that may be incomplete downloads.
overwrite = True

#### FUNCTIONS #################################################################

from ftplib import FTP, error_perm
import os.path, logging

ftp = FTP(ftp_url)


# Acual download function /// this is used if the file meets all of the software checks.
def download(local_filename, remote_size, filename):
    file = open(local_filename, 'wb')
    logging.info('Downloading file: {0} | Filesize: {1} GB'.format(local_filename, round(remote_size/ 1000000000), 2))
    ftp.retrbinary('RETR '+ filename, file.write)
    logging.info(filename, 'downloaded')


# Pull file from FTP site
def ftp_pull(ftp_path):

    # Create new local folder for downloaded Files
    if not os.path.exists(local_path):
        try:
            os.makedirs(local_path)
        except PermissionError:
            logging.info('ERROR: Insuffecient permissions. Unable to make new directory at {0}'.format(local_path))
    logging.info('Downloading files to {0}'.format(local_path))

    # Change directory
    logging.info('Moving to {0}'.format(ftp_path))
    ftp.cwd(ftp_path)

    # Get names of all files in folder
    filenames = ftp.nlst()
    logging.info('Files in folder:{0}'.format(filenames))

    # for loop to get all files in folder
    for filename in filenames:

        # Only downloads files with given extensions
        if filename.endswith(extensions):

            # Get filename and size of remote files
            local_filename = os.path.join(local_path, filename)
            remote_size = ftp.size(filename)

            # Don't download if it already exists
            if os.path.isfile(local_filename):

                # Get the size of the existing file
                local_size = os.stat(local_filename)

                # If local file is smaller than the remote file, delete local and re-download (only if overwrite == True)
                if local_size != remote_size:
                    logging.info('File on server is larger than local file. The previous download may have failed.')

                    # Only delete and re-download if overwrite == True (see config section)
                    if overwrite:
                        logging.info('Overwrite is set to True. Deleting previous files and re-downloading')
                        try:
                            os.remove(local_filename)
                            download(local_filename, remote_size, filename)
                        except PermissionError:
                            logging.info('ERROR: Insuffecient permissions.')
                    else:
                        logging.info('Overwrite is set to False. Existing file has been skipped.')

                logging.info('{0} already downloaded. Skipping.'.format(filename))
                pass
            else:
                download(local_filename, remote_size, filename)


#### MAIN PROGRAM ##############################################################

while True:
    logging.basicConfig(level=logging.DEBUG, filename="ftp-pull-log.txt", filemode="a+",
                            format="%(asctime)-15s %(levelname)-8s %(message)s")
    try: # Try to connect to FTP
        if username == '' and password == '':   # if username and password are blank, don't try to connect with them.
            ftp.login()
        else:
            ftp.login(username, password)       # connect with defined credentials
        logging.info('Connected to FTP client')
    except error_perm:                          # incorrect user config
        logging.info('ERROR: Incorrect login credentials. Please enter the correct FTP username / password and try again.')
        break
    try:
        # if you wish to download multiple files from the URL,
        # simply copy and paste ftp_pull() and create a new file_pull variable
        # in the config section up above. See examples commented below.
        ftp_pull(file_pull)
        #ftp_pull(file_pull-2)
        #ftp_pull(file_pull-3)
    except error_perm:                          # Incorrect directory config
        logging.info('ERROR: The system cannot find the file specified. Please reconfigure the specified directory and try again.')
        break
    ftp.quit()
    logging.info('Disconnected from FTP client. You may now close the window.')
    break
