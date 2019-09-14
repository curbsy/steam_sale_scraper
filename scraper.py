#!/usr/bin/env python

# Author: Makenzie Brian
# Date: February 27, 2018
# Class: ME 599
# File: project > scraper.py
# Description: Pulls steam data and saves to a file

from bs4 import BeautifulSoup as soup
import urllib3
import datetime


def scrape():
    http = urllib3.PoolManager()       # soup stuff
    # if want to be dynamic: url = "http://store.steampowered.com/wishlist/profiles/{}".format(steam_id)
    wishlist_url = "http://store.steampowered.com/wishlist/profiles/76561198823800296/#sort=order"
    response = http.request('GET', wishlist_url)
    page_data = soup(response.data, 'lxml')     # lxml is a faster parser supposedly

    lots_of_data = page_data.find('div', attrs = {'class': 'responsive_page_template_content'})
    #print str(lots_of_data).split("\n")[2][24:].split(",")     # removes other data and label at beginning of line to give app data list
    less_data = str(lots_of_data).split("\n")[2][24:].split(",")        # removes other data and label at beginning of line to give app data list

    # extract ids
    games_list = []
    for item in less_data:
        if "appid" in item:         # split data and remove extra info to get game ids on wishlist
            games_list.append([int(x) for x in item.split(":") if x.isdigit()])
    #print games_list

    game_prices = []
    game_names = []
    file_data, game_count = import_data()
    # print file_data
    for i in xrange(len(games_list)):
        # make urls with ids
        game_url = "http://store.steampowered.com/app/%d" % (games_list[i][0])

        #print game_url
        # get price
        gp, gn = scrape_game(game_url)      #scrape and add data to arrays
        game_prices.append(gp)
        game_names.append(gn)

        # save data to file after pulling data from file
        # file_data, game_count = import_data()
        # #print file_data
        # new_file_data = copy.deepcopy(file_data)
        applist = [int(z[0]) for z in file_data]
        #print applist       # list of game ids form file

        if int(games_list[i][0]) not in applist:
            #print "no"
            file_data.append([str(games_list[i][0]), str(game_names[i]), str(datetime.date.today()),str(game_prices[i])])

        else:            # int(games_list[i][0]) in applist:
            for a, b in enumerate(file_data):
                try:
                    #print games_list[i][0]
                    index_ugh = b.index(str(games_list[i][0]))
                    break
                except ValueError:
                    continue

            #print "yes", a

            #print file_data[a][len(file_data[a]) - 2]
            if file_data[a][len(file_data[a])-2] != str(datetime.date.today()):
                #print "fuck yeah"
                file_data[a].append(str(datetime.date.today()))
                file_data[a].append(str(game_prices[i]))

            #print file_data[a]
            #print file_data

    #put data back in file
    export_data(file_data)


def import_data():
    raw_data = []
    count = 0
    with open("data.csv", "r") as f:
        for line in f:
            raw_data.append(line.strip().split(","))        # list of lists of games data
            count += 1
    #print raw_data, count
    return raw_data, count


def export_data(datums):
    with open("data.csv", "w") as f:
        for lines in datums:
            #f.write(str(lines).replace("'[]", "") + "\n")
            for num in xrange(len(lines)):
                if num < len(lines)-1:
                    f.write(str(lines[num])+",")
                else:
                    f.write(str(lines[num]))
            f.write("\n")


def scrape_game(test_url):
    http = urllib3.PoolManager()       # soup stuff
    response = http.request('GET', test_url)
    page_data = soup(response.data, 'lxml')     # lxml is a faster parser
    price_box = page_data.find('div', attrs={'class': 'game_purchase_price'})

    if price_box is None:           # if on sale is stored in a different attribute
        price_box = page_data.find('div', attrs={'class': 'discount_final_price'})

    price = price_box.text.replace("$","")
    #print float(price)
    name = page_data.find('div', attrs={'class': 'apphub_AppName'}).text
    #print str(name)
    return float(price), str(name)


# MAIN
if __name__ == '__main__':
    #print datetime.date.today()
    scrape()
    #export_data([['297130', 'Titan Souls', '2018-03-18', '3.74', '2018-03-19', '3.74'], ['322500', 'SUPERHOT', '2018-03-18', '24.99', '2018-03-19', '24.99'], ['268910', 'Cuphead', '2018-03-18', '19.99', '2018-03-19', '19.99'], ['367580', 'Hook', '2018-03-18', '0.99', '2018-03-19', '0.81'], ['400', 'Portal', '2018-03-19', '9.99']])
    #scrape_game("http://store.steampowered.com/app/297130/Titan_Souls/")