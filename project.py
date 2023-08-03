import requests
from bs4 import BeautifulSoup
import re
import random
from tabulate import tabulate
import sys
from unidecode import unidecode
import csv
import datetime
import os

url = "https://en.wikipedia.org/wiki/List_of_UEFA_Champions_League_top_scorers"

def main():
    player_names = get_player_names(url)
    names = list(get_names(player_names))
    wikis = list(get_wikis(player_names))
    x = len(names) - 1
    index_list= list(range(0, x))
    os.system('clear')
    print("""
  __            _   _           _ _               _
 / _|          | | | |         | | |             (_)
| |_ ___   ___ | |_| |__   __ _| | |   __ _ _   _ _ ____
|  _/ _ \ / _ \| __| '_ \ / _` | | |  / _` | | | | |_  /
| || (_) | (_) | |_| |_) | (_| | | | | (_| | |_| | |/ /
|_| \___/ \___/ \__|_.__/ \__,_|_|_|  \__, |\__,_|_/___|
                                         | |
                                         |_|
Hello, welcome to footballers guessing game!
You are about to see one of the Champions League top scoring player's club history.
Your task is to find out what player did the program choose for you.
To continue enter your name.
GOOD LUCK!!!
    """)
    p_name = input("Your name: ")
    os.system('clear')
    score = 0
    lifes = 3
    while True:
        if lifes > 0:
            try:
                i = 0
                index = random.choice(index_list)
                player_name = names[index]
                player_wiki = f'https://en.wikipedia.org{wikis[index]}'
                player_hist = get_player_history(player_wiki)
                player_nat = get_player_nat(player_wiki)
                print(player_hist)
                print("❤️" * lifes)
                while True:
                    try:
                        action = int(input(f"""
OK, {p_name}, what would you like to do now?
[0] Guess player's full name
[1] Take a hint
[2] Next player
[3] Quit game
"""))
                        if action == 0:
                            guess = input("""Your guess: """)
                            if guess == unidecode(player_name):
                                if i == 0:
                                    score += 3
                                elif i == 1:
                                    score += 2
                                elif i > 1:
                                    score += 1
                                os.system('clear')
                                print("Congratulations!!!")
                                print(f"Your score: {score}")
                                index_list.remove(index)
                                break

                            else:
                                os.system('clear')
                                print(player_hist)
                                print("❤️" * lifes)
                                print("Try again")
                        elif action == 1:
                            if i == 0:
                                try:
                                    print(f"The player played for {player_nat}")
                                    i += 1
                                except:
                                    print("No data on nationality")
                                    pass
                                    i += 1

                            elif i == 1:
                                print(f"This player's name starts with {str(player_name[0])}")
                                i += 1
                            elif i > 1:
                                print("You're out of hints :(")
                        elif action == 2:
                            os.system('clear')
                            print(f"The player was: {player_name}")
                            index_list.remove(index)
                            lifes -= 1
                            break

                        elif action == 3:
                            os.system('clear')
                            final_score = int(score)
                            hs = highscore(p_name, final_score)
                            sys.exit(f"""
The player was {player_name}
Thank you for playing.
Your final score: {final_score}
{hs}
""")

                    except ValueError:
                        pass
            except ValueError:
                pass
        else:
            final_score = int(score)
            hs = highscore(p_name, final_score)
            sys.exit(f"""
GAME OVER
The player was {player_name}
Your final score: {final_score}
{hs}
""")

def highscore(name, final_score):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    new_entry = {"Name":name,"Score":final_score,"Date":date}
    table = []
    with open("/workspaces/123962438/project/highscore.csv", "r" ) as file:
        lines = csv.DictReader(file)
        for row in lines:
            row_dict = {"Name":row["Name"],"Score":int(row["Score"]),"Date":row["Date"]}
            table.append(row_dict)
    table.append(new_entry)
    fieldnames =["Name","Score","Date"]
    with open("/workspaces/123962438/project/highscore.csv", "w") as file_w:
        writer = csv.DictWriter(file_w, fieldnames=fieldnames)
        writer.writeheader()
        for data in table:
            writer.writerow(data)
    sorted_table = sorted(table, key=lambda x: x['Score'], reverse=True)
    headers = sorted_table[0].keys()
    table_data = [[d[key] for key in headers] for d in sorted_table]
    return tabulate(table_data, headers, tablefmt="heavy_outline")



def get_player_names(url):

    player_names = []
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})
        rows = table.find_all('tr')[1:]

        for row in rows:
            cells = row.find_all(['th', 'td'])
            if len(cells) == 7:
                player_name_cell = cells[1]
                player_name = player_name_cell.find_all('a', {'title': True})
                if player_name:
                    player_names.append(player_name[1])
            elif len(cells) == 6:
                player_name_cell = cells[0]
                player_name = player_name_cell.find_all('a', {'title': True})
                if player_name:
                    player_names.append(player_name[1])
    return player_names

def get_names(player_names):
    names = []

    for player in player_names:
        match_name = re.search(r'<a.*?title=".*">(.*?)<\/a>', str(player))
        name = match_name.group(1)
        names.append(name)
    return names

def get_wikis(player_names):
    wikis= []

    for player in player_names:
        match_name = re.search(r'<a.*?title=".*">(.*?)<\/a>', str(player))
        name = match_name.group(1)
        match_wiki = re.search(r'<a href="(.*?)" title=".*">(.*?)<\/a>', str(player))
        if name == "Francisco Gento":
            wiki = "/wiki/Paco_Gento"
            wikis.append(wiki)
        else:
            if match_wiki:
                wiki = match_wiki.group(1)
                wikis.append(wiki)
    return wikis

def get_player_history(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'infobox vcard'})
    tr = table.find_all(['th','td'], string=re.compile("^Senior career.*?"))
    row = tr[0].parent
    clubs_raw = list(row.next_siblings)
    clubs = []
    for club in clubs_raw:
        if "International career" not in str(club) and "Total" not in str(club):
            clubs.append(club)
        else:
            break
    clubs = clubs[1:]
    i = 1
    table = []
    headers = ["no.", "Span", "Club", "Apps", "Goals"]
    for club in clubs:
        match = re.search(r"(\d{4}.\d{4}|\d{4}-|\d{4})(?:.*\n*).*>(.*)</a>.(\(loan\))?.*\n(\d{1,4}).*\n(\(\d{1,3}\))", str(club))
        try:
            if match.group(3):
                table_row = [i, match.group(1), f'{match.group(2)}{match.group(3)}', match.group(4), match.group(5)]
            else:
                table_row = [i, match.group(1), match.group(2), match.group(4), match.group(5)]
            if table_row[2] == "[i]":
                table_row[2] = "Budapest Honvéd FC"
            table.append(table_row)
            i += 1
        except:
            pass
    table_formatted = tabulate(table, headers, tablefmt="heavy_outline")

    return table_formatted

def get_player_nat(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'infobox vcard'})
    tr = table.find_all(['th','td'], string=re.compile("^Senior career.*?"))
    row = tr[0].parent
    clubs_raw = list(row.next_siblings)
    clubs = []
    for club in clubs_raw:
        if "Managerial career" not in str(club) and "Medal record" not in str(club) and "Signature" not in str(club):
            clubs.append(club)
        else:
            break
    teams = []
    for club in clubs:
        match = re.search(r"(\d{4}.\d{4}|\d{4}-|\d{4})(?:.*\n*).*>(.*)</a>", str(club))
        try:
            teams.append(match.group(2))
        except:
            pass
    x = len(teams) - 1
    if "olympic" in str(teams[x]).casefold():
        x -= 1
    elif "madrid" in str(teams[x]).casefold():
        x -= 2
    return teams[x]

if __name__ == "__main__":
    main()
