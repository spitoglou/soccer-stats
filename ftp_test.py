# nn437wOh3P

from ftplib import FTP

ftp = FTP('spitoglou.byethost9.com', 'spitoglo', 'nn437wOh3P')

ftp.cwd('/soccerstats.csl.gr')
files = ftp.dir()

print(files)

ftp.quit()
