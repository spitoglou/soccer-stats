import os

from dotenv import load_dotenv
from loguru import logger

import ftp_transfer
import soccer1

load_dotenv()


def update_and_upload():
    soccer1.update_local_handout()
    server = os.environ.get("FTP_SERVER", "spitoglou.byethost9.com")
    username = os.environ.get("FTP_USERNAME", "spitoglo")
    remote_dir = os.environ.get("FTP_REMOTE_DIR", "/soccerstats.csl.gr")
    encrypt = False
    monitor = False
    walk = True
    mode = "soccer_update"

    local_dir = "handout"

    p = os.environ["FTP_PASSWORD"]

    try:
        if monitor:
            ftp_transfer.monitor_and_ftp(server, username, p, local_dir, remote_dir, encrypt, walk)
        else:
            ftp_transfer.upload_all(
                server, username, p, local_dir, remote_dir, [], encrypt, walk, mode
            )
    except KeyboardInterrupt:
        logger.warning("Exiting...")


if __name__ == "__main__":
    update_and_upload()
