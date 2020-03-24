#!/usr/bin/env python3

import logging
import os.path
from ftplib import FTP, error_perm
import tqdm as tqdm
from datetime import datetime

# FUNCTIONS ============================================================================================================


# Actual download function /// this is used if the file meets all of the checks in ftp_pull.
def download(local_filename, remote_size, filename):
    logging.info('Downloading file: {0} | File size: {1} GB'.format(filename, round((remote_size / 1000000000), 2)))

    with open(local_filename, 'wb') as file:
        # setup tqdm progress bar with necessary units and such
        with tqdm.tqdm(
                total=remote_size, unit_scale=True, desc='Downloading', unit='bits', position=0, leave=True) as pbar:
            # update tqdm with each block downloaded and saved to file
            def file_write(data):
                file.write(data)
                pbar.update(len(data))
            # Begin download
            ftp.retrbinary('RETR ' + filename, file_write)
            # download confirmation and close file
            logging.info('{0} downloaded.'.format(filename))
            file.close()


# Pull file from FTP site
def ftp_pull(ftp_path, download_folder, extensions, overwrite):
    # Create new local folder for downloaded Files
    if not os.path.exists(download_folder):
        try:
            os.makedirs(download_folder)
        except PermissionError:
            logging.error('PERMISSION ERROR: Unable to make new directory at {0}'.format(download_folder))

    # Change directory
    logging.info('Moving to {0}'.format(ftp_path))
    ftp.cwd(ftp_path)

    # Get names of all files in folder
    ftp_files = ftp.nlst()
    logging.info('Files in folder:{0}'.format(ftp_files))

    # for loop to get all files in folder
    for filename in ftp_files:

        # Only downloads files with given extensions
        if filename.endswith(extensions):

            # Get filename and size of remote files
            local_filename = os.path.join(download_folder, filename)
            remote_size = ftp.size(filename)

            # Don't download if it already exists
            if os.path.isfile(local_filename):

                # Get the size of the existing file
                local_size = os.stat(local_filename).st_size
                logging.info('Remote file size: {0} | Local file size: {1}'.format(remote_size, local_size))

                # If local file is < remote file, delete local and re-download (only if overwrite == True)
                if local_size != remote_size:
                    logging.info('File sizes are not the same. It appears previous download may have failed.')

                    # Only delete and re-download if overwrite == True (see config section)
                    if overwrite:
                        logging.info('Overwrite is set to True. Deleting previous files and re-downloading.')
                        try:
                            os.remove(local_filename)
                            download(local_filename, remote_size, filename)
                        except PermissionError:
                            logging.error('PERMISSION ERROR: You do not have the necessary permissions.')
                    else:
                        logging.info('Overwrite is set to False. Existing file has been skipped.')

                logging.info('File already downloaded. Skipping.')
                pass
            else:
                download(local_filename, remote_size, filename)


def main(username, password, ftp_url, remote_directories, extensions, overwrite):

    # Setup FTP login
    global ftp
    ftp = FTP(ftp_url)

    # What is the current directory (DON'T TOUCH)
    current_dir = os.getcwd()

    # Create timestamp
    timestamp = datetime.now()

    # Download and log folder locations
    download_folder = os.path.join(current_dir, 'downloads')
    log_directory = os.path.join(current_dir, 'logs')

    log_file = os.path.join(log_directory, '{0}_ftp_pull_log.txt'.format(timestamp.strftime('%Y-%m-%d')))

    # Make the log folder if it's not already there
    if not os.path.exists(log_directory):
        try:
            os.makedirs(log_directory)
        except PermissionError:
            print('ERROR: Unable to make new directory at {0}'.format(log_file))

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
        ftp.login(username, password)  # connect with defined credentials
        logging.info('Connected to FTP site {0}'.format(ftp_url))
        logging.info('Downloading location set to {0}'.format(download_folder))
        for directory in remote_directories:
            try:
                ftp_pull(directory, download_folder, extensions, overwrite)
            except error_perm:  # Incorrect directory config
                logging.error('ERROR: The system cannot find the folder specified.')
    except error_perm:  # incorrect user config
        logging.error('ERROR: Incorrect login credentials.')
    ftp.quit()
    logging.info('Disconnected from FTP client. You may now close the window.')
    logging.info('---- END OF SESSION ----')
