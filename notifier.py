#!/usr/bin/env python

# Author: Makenzie Brian
# Date: February 27, 2018
# Class: ME 599
# File: project > notifier.py
# Description:

import smtplib


def import_data():
    raw_data = []
    count = 0
    with open("data.csv", "r") as f:
        for line in f:
            raw_data.append(line.strip().split(","))        # list of lists of games data
            count += 1
    return raw_data, count

def find_em_all():
    file_data, number = import_data()
    temp = [item[2:] for item in file_data]
    prices_ints = [item[1::2]for item in temp]       # gives list of lists of prices
    prices = [[float(j) for j in i] for i in prices_ints]   #convert to floats because I didn't do it before
    #print prices

    low_games = []
    num_count = 0
    for game_price in prices:
        # if last one is lowest in record, return to notify
        #print game_price[len(game_price)-1]
        #print game_price[:1]
        if game_price[len(game_price)-1] < min(game_price[:1]):
            #print file_data[num_count][1]
            #print "yes"
            low_games.append(file_data[num_count][1])         # give line number of lowest new prices because I can
        num_count += 1

    #print num_count
    return low_games

def notify():
    n_games = find_em_all()
    if n_games != []:
        n_games_string = ''.join(n_games)
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.starttls()
        server.login('foxxysoxies@gmail.com', 'Celery225783')

        #print "%s is at its lowest recorded price(s). You should check it out." % n_games_string

        msg = "%s is at its lowest recorded price(s). You should check it out. Please stop sending my emails to spam." % n_games_string
        server.sendmail("foxxysoxies@gmail.com", "kenzie.mae.brian.96@gmail.com", msg)
        server.quit()

# MAIN
if __name__ == '__main__':
    notify()