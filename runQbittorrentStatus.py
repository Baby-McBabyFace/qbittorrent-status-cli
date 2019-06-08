#!/usr/bin/python3

from qbittorrent import Client
from terminaltables import DoubleTable

def speed_value(speed):
    if (speed < 1024):
        return str(speed) +" B/s"
    elif (speed < 1024**2):
        return "{:.2f} KiB/s".format(speed/1024)
    elif (speed < 1024**3):
        return "{:.2f} MiB/s".format(speed/1024**2)
    else:
        return "WTF"

qb = Client("http://localhost:8080/")

downloadSpeed = qb.global_transfer_info["dl_info_speed"]
uploadSpeed = qb.global_transfer_info["up_info_speed"]

table_data = [
    ["qBittorrent-nox"],
    ["qBittorrent-nox Version:", qb.qbittorrent_version],
    ["Total number of torrents: ", len(qb.torrents(filter="all"))],
    ["Total number of Completed torrents: ", len(qb.torrents(filter="completed"))],
    ["Total number of Downloading torrents: ", len(qb.torrents(filter="downloading"))],
    ["Total number of Paused torrents: ", len(qb.torrents(filter="paused"))],
    ["Download Speed: ", speed_value(downloadSpeed)],
    ["Upload Speed: ", speed_value(uploadSpeed)]
    ]
    
table = DoubleTable(table_data)
table.justify_columns[1]="right"
print(table.table)
