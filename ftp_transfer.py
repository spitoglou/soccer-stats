'''
Stavros: Adapted it from here:
https://stackoverflow.com/questions/5663787/upload-folders-from-local-system-to-ftp-using-python-script

This tool will ftp all the files in a given directory to a given location

if the file ftpallcfg.py exists in the directory it will be loaded and the values within it used,
with the current directory used as the source directory.

ftpallcfg.py file contains the following variables.
===========================
server = <server to ftp to>
username = <Username for access to given server>
remote_dir = <remote server directory>
encrypt= True/False
monitor = True/False
walk = True/False
===========================
'''
import ftplib
import os
import socket
import time

from loguru import logger

__revision__ = 1.11

SLEEP_SECONDS = 1


class FtpAddOns:
    PATH_CACHE = set()  # Use set for O(1) lookup instead of list O(N)

    def __init__(self, ftp_h):
        self.ftp_h = ftp_h

    def ftp_exists(self, path):
        '''path exists check function for ftp handler'''
        exists = None
        if path not in self.PATH_CACHE:
            try:
                self.ftp_h.cwd(path)
                exists = True
                self.PATH_CACHE.add(path)  # Use add() for set
            except ftplib.error_perm as e:
                if str(e.args).count('550'):
                    exists = False
        else:
            exists = True

        return exists

    def ftp_mkdirs(self, path, sep='/'):
        '''mkdirs function for ftp handler'''
        split_path = path.split(sep)

        new_dir = ''
        for server_dir in split_path:
            if server_dir:
                new_dir += sep + server_dir
                if not self.ftp_exists(new_dir):
                    try:
                        logger.info('Attempting to create directory (%s) ...' % (new_dir),
                                    self.ftp_h.mkd(new_dir))
                        logger.success('Done!')
                    except Exception as e:
                        logger.exception('ERROR -- %s' % (str(e.args)))


def _get_local_files(local_dir, walk=False, mode=''):
    '''Retrieve local files list
    result_list == a list of dictionaries with path and mtime keys.
        ex: {'path':<filepath>,'mtime':<file last modified time>}
    ignore_dirs == a list of directories to ignore, should not include the base_dir.
    ignore_files == a list of files to ignore.
    ignore_file_ext == a list of extentions to ignore.
    '''
    result_list = []

    ignore_dirs = ['CVS', '.svn']
    ignore_files = ['.project', '.pydevproject']
    ignore_file_ext = ['.pyc']
    if mode == 'soccer_update':
        ignore_file_ext.append('.css')
        ignore_file_ext.append('.ico')
        ignore_file_ext.append('.js')
    logger.info('Mode: ' + mode)
    logger.info(ignore_file_ext)
    base_dir = os.path.abspath(local_dir)

    for current_dir, dirs, files in os.walk(base_dir):
        for this_dir in ignore_dirs:
            if this_dir in dirs:
                dirs.remove(this_dir)

        sub_dir = current_dir.replace(base_dir, '')
        if not walk and sub_dir:
            break

        for this_file in files:
            if this_file not in ignore_files and os.path.splitext(this_file)[-1].lower() not in ignore_file_ext:
                filepath = os.path.join(current_dir, this_file)
                file_monitor_dict = {
                    'path': filepath,
                    'mtime': os.path.getmtime(filepath)
                }
                result_list.append(file_monitor_dict)
    return result_list


def monitor_and_ftp(server,
                    username,
                    password,
                    local_dir,
                    remote_dir,
                    encrypt=False,
                    walk=False):
    '''Monitor local files and when an update is found connect and upload'''
    print('Monitoring changes in (%s).' % (os.path.abspath(local_dir)))
    print('(Use ctrl-c to exit)')

    last_files_list = _get_local_files(local_dir)

    while True:
        try:
            time.sleep(SLEEP_SECONDS)

            latest_files_list = _get_local_files(local_dir)

            files_to_update = []

            for idx in range(len(latest_files_list)):

                if idx < len(last_files_list):
                    # compare last modified times
                    if latest_files_list[idx]['mtime'] > last_files_list[idx]['mtime']:
                        files_to_update.append(latest_files_list[idx])

                else:
                    # add the file to the list (new file)
                    files_to_update.append(latest_files_list[idx])

            if files_to_update:
                print
                print('Detected NEW or CHANGED file(s), attempting to send ...')
                print
                is_success = upload_all(server,
                                        username,
                                        password,
                                        local_dir,
                                        remote_dir,
                                        files_to_update,
                                        encrypt,
                                        walk)

                if not is_success:
                    break

            else:
                print('.',)

            last_files_list = latest_files_list[:]  # copy the list to hold
        except KeyboardInterrupt:
            logger.warning('Exiting.')
            break


def upload_all(server,
               username,
               password,
               base_local_dir,
               base_remote_dir,
               files_to_update=None,
               encrypt=False,
               walk=False, mode=''):
    '''Upload all files in a given directory to the given remote directory'''
    continue_on = False
    login_ok = False
    server_connect_ok = False

    base_local_dir = os.path.abspath(base_local_dir)
    base_remote_dir = os.path.normpath(base_remote_dir)

    if files_to_update:
        local_files = files_to_update
    else:
        local_files = _get_local_files(base_local_dir, walk, mode=mode)

    if local_files:
        ftp_h = ftplib.FTP()

        try:
            ftp_h.connect(server)
            server_connect_ok = True
        except socket.gaierror as e:  # Fixed typo: gaierrora -> gaierror
            logger.exception('ERROR -- Could not connect to (%s): %s' %
                             (server, str(e.args)))
        except OSError as e:
            logger.exception('ERROR -- Could not connect to (%s): %s' %
                             (server, str(e.args)))

        ftp_path_tools = FtpAddOns(ftp_h)

        if server_connect_ok:
            try:
                ftp_h.login(username, password)
                logger.success('Logged into (%s) as (%s)' % (server, username))
                login_ok = True
            except ftplib.error_perm as e:
                logger.exception(
                    'ERROR -- Check Username/Password: %s' % (str(e.args)))
            except ftplib.ProcessTimeout as e:
                logger.exception('ERROR -- Check Username/Password (timeout): %s' %
                                 (str(e.args)))

            if login_ok:

                for file_info in local_files:
                    filepath = file_info['path']

                    path, filename = os.path.split(filepath)
                    remote_sub_path = path.replace(base_local_dir, '')
                    remote_path = path.replace(base_local_dir, base_remote_dir)
                    remote_path = remote_path.replace(
                        '\\', '/')  # Convert to unix style

                    if not ftp_path_tools.ftp_exists(remote_path):
                        ftp_path_tools.ftp_mkdirs(remote_path)

                    # Change to directory
                    try:
                        ftp_h.cwd(remote_path)
                        continue_on = True
                    except ftplib.error_perm as e:
                        logger.exception('ERROR -- %s' % (str(e.args)))
                    except ftplib.PsFtpInvalidCommand as e:
                        logger.exception('ERROR -- %s' % (str(e.args)))

                    if continue_on:
                        if os.path.exists(filepath):
                            display_filename = os.path.join(
                                remote_sub_path, filename)
                            display_filename = display_filename.replace(
                                '\\', '/')

                            logger.info('Sending (%s) ...' %
                                        (display_filename),)
                            send_cmd = 'STOR %s' % (filename)
                            # Use context manager to ensure file handle is closed
                            try:
                                with open(filepath, 'rb') as f_h:
                                    ftp_h.storbinary(send_cmd, f_h)
                                logger.success('Done!')
                            except Exception as e:
                                logger.exception(str(e.args))
                        else:
                            logger.warning("WARNING -- File no longer exists, (%s)!" %
                                           (filepath))

                ftp_h.quit()
                logger.info('Closing Connection')
    else:
        logger.warning('ERROR -- No files found in (%s)' % (base_local_dir))

    return continue_on


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    server = os.environ.get('FTP_SERVER', 'spitoglou.byethost9.com')
    username = os.environ.get('FTP_USERNAME', 'spitoglo')
    remote_dir = os.environ.get('FTP_REMOTE_DIR', '/soccerstats.csl.gr')
    encrypt = False
    monitor = False
    walk = True
    mode = 'soccer_update'

    local_dir = 'handout'

    p = os.environ['FTP_PASSWORD']

    if monitor:
        try:
            monitor_and_ftp(server, username, p, local_dir,
                            remote_dir, encrypt, walk)
        except KeyboardInterrupt:
            logger.warning('Exiting...')
    else:
        try:
            upload_all(server, username, p, local_dir,
                       remote_dir, [], encrypt, walk, mode)
        except KeyboardInterrupt:
            logger.warning('Exiting...')
