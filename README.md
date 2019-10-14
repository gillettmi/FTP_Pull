# FTP_Pull
This is a program written in Python3 that searches for files on a FTP site with a given extension and downloads them to a local folder.

# Instructions
To get this program to work properly, you'll need to provide it with a few variables. By default, the program will skip files that it sees are already saved locally.

**username = 'username'**
Provide your username (if applicable) that you need to login

**password = 'password'**
Provide your password (if applicable) that you need to login

**ftp_url = 'ftp_url'**
Provide the FTP URL that you use to login (don't include http://, just use ftp.[...]

**local_path = './'**
This is where the files will be downloaded to. By default, it saves to the same folder that the main python script is located in.

**file_pull = '/'**
use this to pick where you want to pull files from on the remote server. If it's something other than the home directory, use '~/folder/folder2/folder3'

**extensions**
Write in which file extensions you want to grab. For example, '.mp4', '.mov', '.doc', etc.

**overwrite**
The program is able to determine if a file saved locally and a file saved remotely are the same size. If the ftp is disconnected, it will see that some files are not the correct size. If set to True, it will delete the local file and re-download.

**Repeating the Program**
On line 115, you can see how you can repeat the ftp_pull function to grab things from multiple directories. You can uncomment them and add as many as you like, just be sure to define which directory to pull from in the config section.
