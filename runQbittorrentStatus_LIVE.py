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
    curses.curs_set(0)

    while True:
        downloadSpeed = qb.global_transfer_info["dl_info_speed"]
        uploadSpeed = qb.global_transfer_info["up_info_speed"]

        downloadSessionData = qb.global_transfer_info["dl_info_data"]
        uploadSessionData = qb.global_transfer_info["up_info_data"]

        table_data = [
            ["qBittorrent-nox"],
            ["qBittorrent-nox Version:", "{:>14}".format(qb.qbittorrent_version)],
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
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
        stdscr.addstr(0, 0, time.strftime("%Y-%m-%d | %H:%M:%S"), curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(1, 0, table.table, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(15, 0, "[q] Quit \t[p] Pause all torrents \t[r] Resume all torrents", curses.color_pair(3) | curses.A_BOLD)
        stdscr.refresh()

        keypress = stdscr.getch()

        if keypress == ord("q"):
            break
        elif keypress == ord("p"):
            qb.pause_all()
            stdscr.addstr(20, 0, "All torrents paused!", curses.color_pair(3) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(1)
            stdscr.addstr(20, 0, str(50*" "))
            stdscr.refresh()
        elif keypress == ord("r"):
            qb.resume_all()
            stdscr.addstr(20, 0, "All torrents resumed!", curses.color_pair(3) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(1)
            stdscr.addstr(20, 0, str(50*" "))
            stdscr.refresh()

curses.wrapper(main)
