#!/usr/bin/env python3

# This program automates the downloading of DW programs from a remote FTP site
# Written by Michael Gillett, 2019

import logging
import os.path
from ftplib import FTP, error_perm

# CONFIG ####################################################################

# Login information and server URL /// Input your own information here
username = ''
password = ''
ftp_url = ''

# Where you want the files to save
local_path = './downloads'

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

# Log file location
log_file = 'ftp_pull_log.txt'

# FUNCTIONS #################################################################

ftp = FTP(ftp_url)


# Acual download function /// this is used if the file meets all of the checks in ftp_pull.
def download(local_filename, remote_size, filename):
    file = open(local_filename, 'wb')
    logging.info(
        'Downloading file: {0} | Filesize: {1} GB'.format(local_filename, round((remote_size / 1000000000), 2)))
    logging.info('Downloading file: {0} | Filesize: {1} GB'.format(local_filename, round((remote_size / 1000000000), 2)))
    ftp.retrbinary('RETR ' + filename, file.write)
    logging.info('{0} downloaded.'.format(filename))


# Pull file from FTP site
def ftp_pull(ftp_path):
    # Create new local folder for downloaded Files
    if not os.path.exists(local_path):
        try:
            os.makedirs(local_path)
        except PermissionError:
            logging.error('ERROR: You do not have the necessary permissions. Unable to make new directory at {0}'.format(local_path))

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
                local_size = os.stat(local_filename).st_size
                logging.info('Remote file size: {0} bytes | Local file size: {1} bytes'.format(remote_size, local_size))

                # If local file is < remote file, delete local and re-download (only if overwrite == True)
                if local_size != remote_size:
                    logging.info('File sizes are not the same. It appears previous download may have failed.'.format(remote_size, local_size))

                    # Only delete and re-download if overwrite == True (see config section)
                    if overwrite:
                        logging.info('Overwrite is set to True. Deleting previous files and re-downloading.')
                        try:
                            os.remove(local_filename)
                            download(local_filename, remote_size, filename)
                        except PermissionError:
                            logging.error('ERROR: You do not have the necessary permissions.')
                    else:
                        logging.info('Overwrite is set to False. Existing file has been skipped.')

                logging.info('File already downloaded. Skipping.')
                pass
            else:
                download(local_filename, remote_size, filename)


def main():
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_file,
        filemode='a+',
        format='%(asctime)-15s %(levelname)-8s %(message)s'
    )
    # Define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # Tell the handler to use this format
    console.setFormatter(formatter)
    # Add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logging.info('---- SYSTEM INITIALIZE ----')
    try:  # Try to connect to FTP
        if username == '' and password == '':  # if username and password are blank, don't try to connect with them.
            ftp.login()
        else:
            ftp.login(username, password)  # connect with defined credentials
        logging.info('Connected to FTP client')
        logging.info('Downloading location set to {0}'.format(local_path))
        for directory in remote_directories:
            try:
                ftp_pull(directory)
            except error_perm:  # Incorrect directory config
                logging.error('ERROR: The system cannot find the file specified. Please reconfigure the specified directory and try again.')
    except error_perm:  # incorrect user config
        logging.error('ERROR: Incorrect login credentials. Please enter the correct FTP username, password, or FTP URL and try again.')
    ftp.quit()
    logging.info('Disconnected from FTP client. You may now close the window.')
    logging.info('---- END OF SESSION ----')


# MAIN PROGRAM ##############################################################
if __name__ == '__main__':
    main()
