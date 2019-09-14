#!/usr/bin/env python

# Author: Makenzie Brian
# Date: February 27, 2018
# Class: ME 599
# File: project > does_all_the_things.py
# Description: pulls from other functions to scrape steam for price data, plot said data when requested, and notify the
#              user (me) when a price is the lowest its ever been

from notifier import notify
from plotter import plotty
from scraper import scrape


# MAIN
if __name__ == '__main__':
    scrape()
    notify()
    the_name_of_the_game = raw_input("Enter game name to plot:")
    plotty(the_name_of_the_game)
