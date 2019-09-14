#!/usr/bin/env python

# Author: Makenzie Brian
# Date: February 27, 2018
# Class: ME 599
# File: project > plotter.py
# Description: plots steam sale of specified game (date vs price)

import matplotlib.pyplot as plt

def import_data():
    raw_data = []
    count = 0
    with open("data.csv", "r") as f:
        for line in f:
            raw_data.append(line.strip().split(","))        # list of lists of games data
            count += 1
    #print raw_data, count
    return raw_data, count

def plotty(game_name):
    file_data, count = import_data()

    temp = [item[2:] for item in file_data]
    prices_ints = [item[1::2]for item in temp]       # gives list of lists of prices
    #print prices_ints
    prices = [[float(j) for j in i] for i in prices_ints]   #convert to floats because I didn't do it before
    dates = [item[0::2] for item in temp]       # gives list of lists of dates
    #print dates

    for a, b in enumerate(file_data):
        try:
            # print games_list[i][0]
            index_ugh = b.index(game_name)
            break
        except ValueError:
            continue
    #print "yes", a
    #print file_data[a][1]
    #print prices[a]
    #print dates[a]

    plt.plot(dates[a], prices[a])
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.title('Price of %s' %game_name)
    plt.show()



# MAIN
if __name__ == '__main__':
    plotty('Hook')
