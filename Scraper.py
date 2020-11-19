from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time as time
import datetime
while 1:
    try:
        #Load the html into a variable 'soup'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = 'https://www.rivalry.com/matches/dota-2-betting?'
        req = Request(url=reg_url, headers=headers)
        html = urlopen(req).read() #remember to add a try except thing here

        soup = BeautifulSoup(html, 'html.parser')

        #Find each div container for the live bets
        all_live_bets = soup.find_all('div', attrs={'class': 'bet-line-container bet-line-container-full-size live'})

        #Place all current team neames and odds into lists
        live_names_list = []
        live_odds_list = []

        for live_bet in all_live_bets:
            names = live_bet.find_all('div', attrs={'class': 'team-name'})
            live_names_list.append([])
            for name in names:
                live_names_list[-1].append(name.string)
            odds = live_bet.find_all('span', attrs={'class': 'odds'})
            live_odds_list.append([])
            for odd in odds:
                live_odds_list[-1].append(odd.string)

        #Read the active bets csv file
        active_games_list = []
        with open('active.csv', newline='') as csvfile:
            active = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in active:
                active_games_list.append(row)

        #write the no longer active games to file
        for game in active_games_list:
            if [game[0], game[1]] in live_names_list:
                pass
            else:
                game.append(-1)
                game.append(-1)
                with open('completed.csv', mode='a+', newline='') as csvfile:
                    active_writer = csv.writer(csvfile)
                    active_writer.writerow(game)

        #delete the no longer active games from the active_games_list
        active_games_list = [game for game in active_games_list if [game[0], game[1]] in live_names_list]

        #add active games from live list to active list if needed
        if active_games_list == []:
            for name in live_names_list:
                active_games_list.append(name)
        else:
            for name in live_names_list:
                for game in active_games_list:
                    if name == [game[0], game[1]]:
                        break
                    if game == active_games_list[-1]:
                        active_games_list.append(name)

        #add odds to the active games list
        for game, odds in zip(active_games_list, live_odds_list):
            if odds == [] and game != []:
                odds.append(-1)
                odds.append(-1)
            game.append(odds[0])
            game.append(odds[-1])

        #print lists
        print(datetime.datetime.now())
        print('Live odds list is ' + str(live_odds_list))
        print('Live games list is ' + str(live_names_list))
        i = 0
        for game in active_games_list:
            i += 1
            print('Active game number {}: {}'.format(i, game))

        with open('active.csv', mode='w', newline='') as csvfile:
            active_writer = csv.writer(csvfile)
            active_writer.writerows(active_games_list)

        if len(live_names_list) == 0 and len(active_games_list) == 0:
            time.sleep(300)

        time.sleep(120)

    except Exception as e:
        print(e)
        time.sleep(5)

