# FTP_Pull
This is a program written in Python3 that searches for files on a FTP site with a given extension and downloads them to a local folder. This program uses ftplib to access the server as well as logging to save a program log.

# Dependencies
This program relies on tqdm to work and show the progress of the downloading files. Run `pip install tqdm` using your computer's terminal to install it.

# How-To
To use the program properly, you'll need to provide it with a few variables. Here's what you can change:

**username** The username that you use to login to your FTP site

**password** The password to login to your FTP site

**ftp_url** The URL that you use to access the FTP site. Don't include ftp://, just do ftp.website.com

**local_path** This is where the program will save the files it finds on the remote site to your local computer. You can also do network storages too. The default is set to './downloads', which will be in the same folder that the ftp_pull.py file is located. If this folder doesn't exist, the program will make it.

**remote_directories** This list includes all of the folders that you want to pull from. If you want to search multiple directories for files, simply uncomment the first two lines and add in your file structure here. Just make sure to include '~/' in the beginning, that way it always returns to home and brances out from there.

**extensions** The program will only search for files with the correct extensions. It's currently configured to search for video files, but you can change that to whatever you want.

**overwrite** If set to True, the program will overwrite any local files that are not the same size as the remote files. If the program is disconnected for any reason, you can enable this to overwrite files that we're completely downloaded.

**log_file** is where the program will save it's log file. Default is in the same folder as the downloads folder

# Help
If you need help, feel free to send me a message on GitHub. I'm still working out a few kinks in the program, so any constructive criticism is greatly appreciated.
