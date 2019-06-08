#!/usr/bin/python3

import time
import curses
from qbittorrent import Client
from terminaltables import AsciiTable

def speed_value(speed):
    if (speed < 1024):
        return str(speed) +" B/s"
    elif (speed < 1024**2):
        return "{:.2f} KiB/s".format(speed/1024)
    elif (speed < 1024**3):
        return "{:.2f} MiB/s".format(speed/1024**2)
    else:
        return "WTF"

def session_data_value(data_session):
    if (data_session < 1024):
        return str(data_session) +" B"
    elif (data_session < 1024**2):
        return "{:.2f} KiB".format(data_session/1024)
    elif (data_session < 1024**3):
        return "{:.2f} MiB".format(data_session/1024**2)
    elif (data_session < 1024**4):
        return "{:.2f} GiB".format(data_session/1024**3)
    elif (data_session < 1024**5):
        return "{:.2f} TiB".format(data_session/1024**4)
    else:
        return "WTF"

qb = Client("http://localhost:8080/")

def main(stdscr):
    stdscr.nodelay(1)

    while True:
        downloadSpeed = qb.global_transfer_info["dl_info_speed"]
        uploadSpeed = qb.global_transfer_info["up_info_speed"]

        downloadSessionData = qb.global_transfer_info["dl_info_data"]
        uploadSessionData = qb.global_transfer_info["up_info_data"]

        table_data = [
            ["qBittorrent-nox"],
            ["qBittorrent-nox Version:", qb.qbittorrent_version],
            ["Total number of torrents: ", len(qb.torrents(filter="all"))],
            ["Total number of Completed torrents: ", len(qb.torrents(filter="completed"))],
            ["Total number of Downloading torrents: ", len(qb.torrents(filter="downloading"))],
            ["Total number of Paused torrents: ", len(qb.torrents(filter="paused"))],
            ["Download Speed: ", speed_value(downloadSpeed)],
            ["Upload Speed: ", speed_value(uploadSpeed)],
            ["Session Download: ", session_data_value(downloadSessionData)],
            ["Session Upload: ", session_data_value(uploadSessionData)]
            ]

        table = AsciiTable(table_data)
        table.justify_columns[1]="right"
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        stdscr.addstr(1, 0, table.table, curses.color_pair(1))
        stdscr.refresh()

        if stdscr.getch() == ord('q'):
            break

curses.wrapper(main)
