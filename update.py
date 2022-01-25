import soccer1
import ftp_transfer
from loguru import logger


def update_and_upload():
    soccer1.update_local_handout()
    server = 'spitoglou.byethost9.com'
    username = 'spitoglo'
    remote_dir = '/soccerstats.csl.gr'
    encrypt = False
    monitor = False
    walk = True
    mode = 'soccer_update'

    local_dir = 'handout'

    # get the user password
    p = 'nn437wOh3P'

    try:
        if monitor:
            ftp_transfer.monitor_and_ftp(server, username, p, local_dir,
                                         remote_dir, encrypt, walk)
        else:
            ftp_transfer.upload_all(server, username, p, local_dir,
                                    remote_dir, [], encrypt, walk, mode)
    except KeyboardInterrupt:
        logger.warning('Exiting...')


if __name__ == "__main__":
    update_and_upload()
